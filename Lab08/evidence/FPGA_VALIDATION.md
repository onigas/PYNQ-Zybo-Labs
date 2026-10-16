# Lab08.3 — Recorded Zybo FPGA validation (formerly Lab08.4)

This is the **saved output from the original on-board notebook**, not a new measurement or a regenerated simulation. Board: Digilent Zybo Legacy (XC7Z010), PYNQ 3.0.1. FPGA image `compact_gtsrb.bit` (Vivado 2022.2).

The full original user notebook with execution output was supplied as `Lab08.4_BNN_FPGA_Inference_GTSRB.ipynb`; its code is reflected in the renumbered Lab08.3 notebook. The originally recorded data are transcribed here to avoid losing verification evidence if notebook outputs are cleared.

## Hardware results

- FPGA overlay loaded; AXI DMA `axi_dma_0` at `0x41e00000`.
- AXI DMA test pattern: complete transfer, 44 signed int16 score values (88 output bytes).
- Official GTSRB `00105.ppm`: real class **4**; predicted class **4**; end-to-end time **23.79 ms**.
- Logitech C270: successfully acquired a `480 × 640` frame and produced an FPGA prediction **38**; ground truth for this live input was *not* established.
- The software BNN from Lab08.2 is **not** the same network. Do **not** treat ARM-vs-FPGA latency as a same-network speedup.

## Original 20-image test output

| # | GTSRB CSV row | Actual | FPGA | Result | DMA + inference (ms) |
|---:|---:|---:|---:|---|---:|
| 1 | 10406 | 0 | 3 | Incorrect | 22.6 |
| 2 | 2335 | 1 | 1 | Correct | 22.6 |
| 3 | 419 | 2 | 4 | Incorrect | 22.5 |
| 4 | 8977 | 3 | 9 | Incorrect | 22.7 |
| 5 | 4758 | 4 | 4 | Correct | 22.5 |
| 6 | 5877 | 5 | 2 | Incorrect | 22.6 |
| 7 | 1065 | 7 | 12 | Incorrect | 22.6 |
| 8 | 4787 | 8 | 8 | Correct | 23.4 |
| 9 | 8466 | 9 | 9 | Correct | 23.3 |
| 10 | 4361 | 10 | 10 | Correct | 23.3 |
| 11 | 10448 | 11 | 30 | Incorrect | 23.3 |
| 12 | 9448 | 12 | 12 | Correct | 23.3 |
| 13 | 8920 | 13 | 13 | Correct | 22.6 |
| 14 | 11315 | 14 | 14 | Correct | 22.5 |
| 15 | 8710 | 17 | 17 | Correct | 24.9 |
| 16 | 2425 | 18 | 18 | Correct | 22.5 |
| 17 | 11536 | 20 | 20 | Correct | 25.0 |
| 18 | 8166 | 25 | 1 | Incorrect | 22.6 |
| 19 | 1057 | 33 | 33 | Correct | 25.5 |
| 20 | 3700 | 35 | 35 | Correct | 22.6 |

**Saved result:** **13/20 correct (65%)**, **23.15 ms/image** mean end-to-end time. The sample is small and nonrepresentative of full GTSRB test-set performance.

## Supplied-file checksums (SHA-256)

| File | Bytes | SHA-256 |
|---|---:|---|
| `compact_gtsrb.bit` | 2,083,852 | `08d4ae460844fd05f74e6389458ca5b6a07f8591739f27c06ed4610b152ce657` |
| `compact_gtsrb.hwh` | 579,702 | `091c884e4bf208259cca8df063e0b8cad909645b3d1c650301752f1bc4bc0e00` |
| `gtsrb_batch20_inputs.npz` | 50,619 | `6c9d94208a92a7eda5fb1689b915b5ea897caf24ce950234f02f54f981c89016` |
