# Lab06 – Introduction to Hardware Acceleration

**Platform:** Digilent Zybo **legacy** (Zynq-7010, `xc7z010clg400-1`), PYNQ 3.0.1, Vivado 2022.2.

## Laboratory sequence

| Notebook | Objective | Overlay |
|---|---|---|
| [06.1 – PS–PL Architecture](notebooks/Lab06.1_PS_PL_Architecture.ipynb) | Inspect PS and PL metadata, AXI IP and addresses | `base.bit` |
| [06.2 – AXI Register Access](notebooks/Lab06.2_AXI_Register_Access.ipynb) | Direct MMIO access to LEDs via AXI GPIO | `base.bit` |
| [06.3 – Custom Hardware Accelerator](notebooks/Lab06.3_Custom_Hardware_Accelerator.ipynb) | Compute `Y=A×B+C` in PL and test output | `lab06.bit` and `lab06.hwh` |
| [06.4 – ARM vs FPGA Performance](notebooks/Lab06.4_ARM_vs_FPGA_Performance.ipynb) | Compare single-operation AXI overhead to internally batched MAC, including a hardware cycle counter | Both `lab06` and `lab06_batch` |

Every code cell is preceded by a Markdown explanation. **06.1–06.3 were tested on the Zybo**, and the batch extension of **06.4 was run on the board** with the measured example shown below.

## Hardware sources

- [`hardware/build_lab06.tcl`](hardware/build_lab06.tcl) + [`hardware/rtl/mac8.v`](hardware/rtl/mac8.v): original single-operation MAC; leave the original `base.bit` unchanged.
- [`hardware/build_lab06_batch.tcl`](hardware/build_lab06_batch.tcl) + [`hardware/rtl/batch_mac.v`](hardware/rtl/batch_mac.v): independent batch-MAC overlay with an internal cycle counter.
- [Hardware README](hardware/README.md): Vivado setup, register map, testbench and safety notes.
- Both accelerators have simulation testbenches in `hardware/rtl/`.

## Deployment on Zybo

1. Use the **original Digilent Zybo board files**, not Zybo Z7-10.
2. With **Vivado 2022.2**, run both scripts from the Tcl Console:
   ```tcl
   source {C:/path/to/Lab06/hardware/build_lab06.tcl}
   source {C:/path/to/Lab06/hardware/build_lab06_batch.tcl}
   ```
3. The scripts generate four files in `hardware/output/`: `lab06.bit`, `lab06.hwh`, `lab06_batch.bit`, `lab06_batch.hwh`.
4. In Jupyter on Zybo, create `Lab06/notebooks` and upload the four notebooks into `Lab06/notebooks/`, and copy **both .bit/.hwh pairs** into `Lab06/overlays/` (or beside the notebooks, for backward compatibility).
5. Execute notebooks 06.1 to 06.4 in order. Reloading an overlay reprograms FPGA logic; previously created MMIO mappings must not be reused after a different overlay is loaded.

**Bitstream availability:** the instructor has provided and validated all four generated files, but they have **not yet been committed to this repository**. Their SHA-256 checksums are documented in [`overlays/README.md`](overlays/README.md). Until the binaries are published, build both overlay pairs from source or obtain the verified files from the instructor. Keep `.bit` and `.hwh` as matched pairs.

## Benchmark interpretation

Notebook 06.4 includes **two contrasting experiments**:

- **Part A:** a single MAC through multiple AXI register accesses. Hardware calls can take longer than the arithmetic computed by Python.
- **Part B:** `N` MAC operations generated and executed internally in FPGA after one launch. The FPGA cycle counter reports the compute duration independently from the total Python/AXI service time.

A previous run on Zybo produced:

| N | Python (µs) | FPGA+AXI (µs) | FPGA only (µs) | Speedup against Python |
|---:|---:|---:|---:|---:|
| 100 | 485.72 | 159.05 | 1.00 | 3.05× |
| 1,000 | 4,867.26 | 165.59 | 10.00 | 29.39× |
| 10,000 | 48,755.25 | 206.13 | 100.00 | 236.53× |
| 100,000 | 474,617.20 | 1,103.38 | 1,000.00 | 430.15× |

The table documents **one measured run, not expected fixed results**. The latest notebook also times **final result-register readback**, so repeat-run totals may differ.

At the configured **100 MHz**, 100,000 hardware cycles correspond to **1 ms of internal computation**. The end-to-end overhead includes Python, Linux scheduling, AXI, polling, and reads. The speedup is relative to **an interpreted Python loop**, *not* optimized compiled ARM C. Inputs are generated inside the FPGA, so this is not yet a test of image transfer performance. Lab07 will address data movement.

## Validation

- Lab06.1–06.3: reported functional on the physical Zybo board.
- Original MAC: 100/100 additional randomized tests passed.
- Batch MAC: correct functional output and performance measurements reported from the physical Zybo.
- The original laboratory environment and generated bitstream files are not available in this chat; the Vivado implementation timing report (WNS) has not been independently inspected. Verify timing closure before classroom use.
