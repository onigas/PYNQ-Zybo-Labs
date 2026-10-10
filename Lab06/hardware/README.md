# Hardware for Lab06 – Zybo Legacy

Target hardware: **Digilent Zybo legacy** (`xc7z010clg400-1`), built with **Vivado 2022.2**.

## Prerequisites

Install original Zybo board definitions: https://github.com/Digilent/vivado-boards/tree/master/new/board_files/zybo . Do not select Zybo Z7-10. Verify the board preset in Vivado before launching synthesis.

## Build two independent overlays

From the **Vivado Tcl Console**, with the appropriate Windows path:

```tcl
source {C:/path/to/Lab06/hardware/build_lab06.tcl}
source {C:/path/to/Lab06/hardware/build_lab06_batch.tcl}
```

The first script creates `hardware/build/` and produces `output/lab06.bit` and `output/lab06.hwh`. The second script creates a **different project**, `hardware/build_batch/`, and produces `output/lab06_batch.bit` and `output/lab06_batch.hwh`. It does not overwrite the first overlay.

Check **implementation timing** (WNS >= 0 at 100 MHz) before deploying these designs.

## Architecture and register map

### Single MAC

`mac8.v` implements combinational unsigned **Y = A×B+C**, with A,B 8 bits and C 16 bits. Its physical AXI addresses are obtained dynamically from the generated HWH metadata:

| IP | Channel 1 DATA offset | Channel 2 DATA offset |
|---|---|---|
| `operands_gpio` | `0x00`: A | `0x08`: B |
| `c_gpio` | `0x00`: C | n/a |
| `result_gpio` | `0x00`: Y | n/a |

### Batch MAC

`batch_mac.v` uses a 100 MHz PL clock. The ARM programs N and sends a START pulse. The FPGA generates its A/B/C sequence internally and executes **N** multiply-accumulate operations (one per busy clock cycle). The result SUM wraps modulo 2³²; a hardware counter returns **CYCLES = N**.

The sequence starts at A=B=C=SUM=0, then for every MAC:
```
SUM = (SUM + A*B + C) modulo 2^32
A = (A + 17) modulo 256
B = (B + 53) modulo 256
C = (C + 997) modulo 65536
```

| AXI GPIO IP | DATA channel 1 (`0x00`) | DATA channel 2 (`0x08`) |
|---|---|---|
| `control_gpio` | N, 32-bit output | START, bit 0 output |
| `results_gpio` | SUM, 32-bit input | CYCLES, 32-bit input |
| `status_gpio` | bit 0 DONE, bit 1 BUSY | not used |

GPIO direction-register offsets are `0x04` (channel 1) and `0x0C` (channel 2). Direction zero means output, direction one means input. Write START 0→1→0; DONE persists until the next accepted rising edge.

At 100 MHz, one clock cycle is 10 ns and 100,000 active cycles correspond to 1 ms. The **internal FPGA time excludes AXI transactions**.

## Simulation

From `Lab06/hardware` with Icarus Verilog, if installed:

```sh
iverilog -g2012 -s tb_mac8 -o mac_tb rtl/mac8.v rtl/tb_mac8.v
vvp mac_tb
iverilog -g2012 -s tb_batch_mac -o batch_tb rtl/batch_mac.v rtl/tb_batch_mac.v
vvp batch_tb
```

The batch testbench covers N=0,1,2,7,100,4096,100000 and checks cycle counts and accumulated sums. You may instead use Vivado's built-in simulator.

## Interpreting timing correctly

The batch notebook measures end-to-end host time **including register writes, START, DONE polling and reading SUM and CYCLES**. Subtracting the FPGA compute duration yields combined *Python/OS/MMIO/AXI overhead*; it is not the pure bus transport latency.

**Scope:** the batch engine generates operands *inside the FPGA*. It intentionally avoids per-operand AXI traffic and illustrates overhead amortization, not a general streaming-image acceleration benchmark. Comparing against an optimized ARM implementation in C is a separate experiment.

The generated `.bit` and `.hwh` files are not distributed with this source package; generate them locally and copy the matching pairs beside the notebooks. Reprogramming PL invalidates MMIO mappings of the previous overlay.
