"""Lab07: minimal, inspectable PYNQ 3.0.1 AXI DMA threshold driver.

The FPGA processes four packed uint8 pixels per 32-bit AXI-Stream beat.
The helper performs no silent CPU fallback: missing FPGA hardware raises errors.
"""
from pathlib import Path
from time import perf_counter_ns, monotonic

import numpy as np


def reference_threshold(image, threshold):
    """CPU reference: 255 if pixel >= threshold, otherwise zero."""
    img = np.asarray(image)
    if img.ndim != 2 or img.dtype != np.uint8:
        raise ValueError("Expected a two-dimensional uint8 grayscale image")
    threshold = int(threshold)
    if not (0 <= threshold <= 255):
        raise ValueError("Threshold must be between 0 and 255")
    return np.where(img >= threshold, 255, 0).astype(np.uint8)


def locate_overlay():
    """Find matched bitstream and HWH relative to the notebook working directory."""
    for directory in (Path("../overlays"), Path("overlays"), Path(".")):
        bit = directory / "lab07.bit"
        hwh = directory / "lab07.hwh"
        if bit.is_file() and hwh.is_file():
            return bit.resolve(), hwh.resolve()
    raise FileNotFoundError(
        "lab07.bit and lab07.hwh missing: generate them in Vivado and copy "
        "the matching pair into Lab07/overlays/ (or next to the notebook)."
    )


class ThresholdDMA:
    """DMA threshold engine; a new instance loads the FPGA overlay."""

    def __init__(self):
        # Late imports keep the reference algorithm executable on a regular PC.
        from pynq import MMIO, Overlay, allocate

        self._allocate = allocate
        bit, _ = locate_overlay()
        self.overlay = Overlay(str(bit))
        if "axi_dma_0" not in self.overlay.ip_dict:
            raise RuntimeError("HWH does not describe axi_dma_0")
        if "threshold_gpio" not in self.overlay.ip_dict:
            raise RuntimeError("HWH does not describe threshold_gpio")
        self.dma = self.overlay.axi_dma_0
        info = self.overlay.ip_dict["threshold_gpio"]
        self._gpio = MMIO(info["phys_addr"], info.get("addr_range", 0x1000))
        self._gpio.write(0x04, 0)  # all eight threshold bits are outputs
        self._gpio.write(0x00, 128)

    def process(self, image, threshold=128):
        """Return (mask, times) without any software fallback.

        times contains prep_us, dma_us and total_us. total_us includes
        input preparation, buffer allocation, AXI start/wait and output copy.
        dma_us is ONLY host-observed DMA start/wait, not FPGA-only compute time.
        """
        gray = np.asarray(image)
        if gray.dtype != np.uint8 or gray.ndim != 2:
            raise ValueError("Expected an H x W image with dtype uint8")
        height, width = gray.shape
        if height == 0 or width == 0 or width % 4:
            raise ValueError("Image width must be a positive multiple of four pixels")
        th = int(threshold)
        if not (0 <= th <= 255):
            raise ValueError("Threshold must be an integer between 0 and 255")
        nbytes = height * width
        maximum = getattr(self.dma, "buffer_max_size", (1 << 23) - 1)
        if nbytes > maximum:
            raise ValueError("Frame has {} bytes; DMA allows at most {} per transaction".format(nbytes, maximum))

        start_ns = perf_counter_ns()
        source = np.ascontiguousarray(gray).reshape(-1)
        # No DRE is needed: pynq.allocate returns aligned 32-bit buffers,
        # and the frame contains a whole number of 32-bit words.
        input_buffer = self._allocate(shape=(nbytes // 4,), dtype=np.uint32)
        output_buffer = self._allocate(shape=(nbytes // 4,), dtype=np.uint32)
        try:
            input_buffer.view(np.uint8)[:] = source
            output_buffer[:] = 0
            self._gpio.write(0x00, th)
            prep_end = perf_counter_ns()
            # Start S2MM BEFORE MM2S: the receiver must be ready for TLAST.
            self.dma.recvchannel.transfer(output_buffer)
            self.dma.sendchannel.transfer(input_buffer)
            # PYNQ's .wait() can block indefinitely when a faulty RTL omits
            # TLAST. Explicitly enforce a deadline before calling .wait().
            deadline = monotonic() + 5.0
            while not (self.dma.sendchannel.idle and self.dma.recvchannel.idle):
                if self.dma.sendchannel.error or self.dma.recvchannel.error:
                    raise RuntimeError('DMA reported an error; check the Vivado AXI stream wiring and TLAST')
                if monotonic() >= deadline:
                    mmio = self.dma.mmio
                    tx = mmio.read(0x04)  # MM2S_DMASR
                    rx = mmio.read(0x34)  # S2MM_DMASR
                    raise TimeoutError('DMA timeout: MM2S status 0x{:08X}, S2MM status 0x{:08X}. '
                                       'Check TLAST, AXI clocks and HP0 mapping; reload the overlay '
                                       'before retrying.'.format(tx, rx))
            self.dma.sendchannel.wait()
            self.dma.recvchannel.wait()
            dma_end = perf_counter_ns()
            mask = output_buffer.view(np.uint8).reshape(height, width).copy()
            end_ns = perf_counter_ns()
        finally:
            input_buffer.close()
            output_buffer.close()
        times = {
            "prep_us": (prep_end - start_ns) / 1000.0,
            "dma_us": (dma_end - prep_end) / 1000.0,
            "total_us": (end_ns - start_ns) / 1000.0,
        }
        return mask, times
