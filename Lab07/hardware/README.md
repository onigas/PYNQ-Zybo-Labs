# Lab07 hardware: AXI-Stream grayscale threshold processor

**Target:** Digilent **original Zybo legacy** (Zynq-7010, `xc7z010clg400-1`), Vivado **2022.2** and PYNQ **3.0.1**.

## Why another FPGA design?

The Lab06 accelerator sends each operand separately through AXI GPIO. Here the ARM sends an entire image as **packed 32-bit words** using AXI DMA. The FPGA processes four 8-bit grayscale pixels simultaneously on each accepted AXI4-Stream beat.

For each input pixel `p`, output `255` if `p >= threshold`; otherwise `0`. Data packing is four adjacent pixels per 32-bit word. The accelerator preserves `TKEEP` and `TLAST`, and its one-register pipeline handles AXI-stream `TREADY` backpressure.

## Diagram

```text
ARM A9 / Python       Programmable Logic (PL)                DDR
  control   --AXI GP0--> [AXI DMA registers, AXI GPIO]      |
  threshold --AXI GP0--> [threshold_gpio]                   |
                       [AXI DMA MM2S] <--- PS HP0 <---------+
                               | AXI-Stream 32 bits         |
                     [threshold_axis: 4 px / beat]           |
                               | AXI-Stream 32 bits         |
                       [AXI DMA S2MM] ---> PS HP0 ----------+
```

The theoretical maximum of the core is four pixels per accepted clock at 100 MHz; **this is not the measured end-to-end system throughput**. AXI, DDR and Python introduce overhead, and DMA transfers can stall.

## Vivado build

Install original Digilent Zybo board files (not Zybo Z7-10) for Vivado 2022.2. Open **Tcl Console** and run:

```tcl
source {C:/path/to/Lab07/hardware/build_lab07.tcl}
```

The Tcl script creates a separate project `hardware/build/` and outputs:

```text
hardware/output/lab07.bit
hardware/output/lab07.hwh
```

Do not use Lab06 bitstreams in Lab07. Copy **both** generated files to `Lab07/overlays/`, preserving identical stems. Do not publish a bitstream before checking that implementation has passed timing (`WNS >= 0`).

## Hardware register map / data constraints

- `threshold_gpio`: AXI GPIO channel 1 DATA register `0x00`, TRI register `0x04`; GPIO width **8-bit output**.
- `axi_dma_0`: simple-mode AXI DMA, with MM2S and S2MM enabled, 32-bit streaming, **no scatter-gather**, transfer length width **23**.
- `threshold_axis_0`: custom Verilog, 32-bit input and output; handles AXI4-Stream `TDATA`, `TKEEP`, `TVALID`, `TREADY`, `TLAST`.
- Clock: 100 MHz PL FCLK0; DDR access through PS **HP0**, register control through **GP0**.
- Student frames must be grayscale `uint8`, contiguous, and their width must be divisible by **4**. This implementation deliberately avoids partial last words.
- Frame size must not exceed `dma.buffer_max_size` (less than 2²³ bytes for the script configuration).
- Set threshold *between frames*, not during a running transfer.

## Testbench

`rtl/tb_threshold_axis.v` sends 32 beats (128 bytes) through the RTL, checks every output byte and `TLAST` and deliberately throttles `M_AXIS_TREADY` to verify backpressure. Run in Vivado **Run Simulation → Run Behavioral Simulation** with `tb_threshold_axis` as top, or with Icarus Verilog if available:

```sh
iverilog -g2012 -s tb_threshold_axis -o threshold_tb rtl/threshold_axis.v rtl/tb_threshold_axis.v
vvp threshold_tb
```

Expected end line: `PASS: 32 streaming beats, 128 pixels, TLAST and backpressure`.

## Validation

The instructor confirmed successful execution on a physical **Zybo legacy** of notebooks 07.1, 07.2 and 07.3, including the revised color detection demonstration and the generated `lab07.bit`/`lab07.hwh` pair. The timing-closure report has not been independently reviewed.

**Release state:** The RTL, Vivado project builder, software driver, and the tested FPGA bitstream/HWH pair are published in this repository. Ready-to-use `lab07.bit` and `lab07.hwh` are in [`Lab07/overlays/`](../overlays/). Students can run 07.2 and 07.3 without generating a new bitstream. Timing closure reports have not been independently audited; check implementation timing when rebuilding hardware.
