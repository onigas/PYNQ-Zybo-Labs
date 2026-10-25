# Hardware–Software Co-design — FPGA Project Proposals

**Repository:** PYNQ-Zybo-Labs  
**Target platforms:** Digilent Zybo Legacy / Digilent PYNQ-Z2 (as indicated)  
**Suggested duration:** 4–5 weeks  
**Development:** PYNQ Python / Jupyter notebooks; existing precompiled FPGA overlays

The **13 project ideas** are listed below. Each detailed page prioritizes a **specific existing implementation with a direct source link**, to be reproduced and explained. Projects lacking a confirmed notebook and compatible precompiled overlay are **not yet ready for allocation**.

| Code | Project title | Implementation board |
| --- | --- | --- |
| HW-01 | [FPGA-Based Sensor Calibration and Arithmetic Processing](Details/HW-01.md) | Zybo Legacy |
| HW-02 | [Programmable Digital Waveform Generator Using Logictools](Details/HW-02.md) | PYNQ-Z2 |
| HW-03 | [FIR Filter Accelerator](Details/HW-03.md) | PYNQ-Z2 |
| HW-04 | [FFT Spectrum Analyzer Accelerator](Details/HW-04.md) | Zybo Legacy / PYNQ-Z2 |
| HW-05 | [PS-Controlled Audio Processing](Details/HW-05.md) | PYNQ-Z2 preferred; Zybo Legacy if audio interface verified |
| HW-06 | [Sobel Edge Detection Accelerator](Details/HW-06.md) | Zybo Legacy / PYNQ-Z2 |
| HW-07 | [Programmable 2D Convolution Accelerator](Details/HW-07.md) | Zybo Legacy / PYNQ-Z2 |
| HW-09 | [FPGA Sensor Data Preprocessing](Details/HW-09.md) | Zybo Legacy / PYNQ-Z2; external sensor optional |
| HW-10 | [Real-Time Signal Anomaly Detector](Details/HW-10.md) | Zybo Legacy / PYNQ-Z2 |
| HW-11 | [Matrix Operations Accelerator](Details/HW-11.md) | Zybo Legacy / PYNQ-Z2 |
| HW-12 | [Image Histogram Accelerator](Details/HW-12.md) | Zybo Legacy / PYNQ-Z2 |
| HW-13 | [Run-Length Encoding Compression Accelerator](Details/HW-13.md) | Zybo Legacy / PYNQ-Z2 |
| HW-14 | [ECG QRS Detection Accelerator](Details/HW-14.md) | Zybo Legacy / PYNQ-Z2 |

## Source Verification Status

| Project | Concrete starting point | Status |
| --- | --- | --- |
| HW-10 | [Lab08 BNN accelerator and notebook](../../Lab08/README.md) | No complete matching anomaly-detection overlay confirmed |
| HW-11 | [Lab06 MAC and batch MAC](../../Lab06/README.md) | Existing Lab06 MAC implementation; optional public advanced accelerator to investigate |
| HW-12 | [Lab07.2 DMA threshold accelerator](../../Lab07/notebooks/Lab07.2_AXIDMA_Threshold_Accelerator.ipynb) | Adaptation of Lab07 thresholding; not a dedicated histogram accelerator |
| HW-13 | [Lab07 — example of PS/PL DMA data transfer](../../Lab07/README.md) | No complete public RLE notebook with compatible bit/hwh confirmed |
| HW-14 | [Course Lab03 XADC and data logging](../../Lab03/README.md) | No complete public QRS-processing notebook with compatible overlay confirmed |
| HW-01 | [Lab06 complete MAC accelerator and notebooks](../../Lab06/README.md) | Existing course implementation |
| HW-02 | [Adam Taylor — Signal Generation and Logic Tracing](https://medium.com/@aptaylorceng/pynq-edition-signal-generation-and-logic-tracing-599c62891bc3) | Official PYNQ-Z2 Logictools overlay; reproduce Pattern Generator + Trace Analyzer |
| HW-03 | [soheilbh/fir_accel_pynq — complete repository](https://github.com/soheilbh/fir_accel_pynq) | Concrete public reproductions available for PYNQ-Z2 |
| HW-04 | [Existing course DMA workflow — Lab07](../../Lab07/README.md) | Complete public FFT notebook plus precompiled overlay not yet verified |
| HW-05 | [PYNQ official documentation](https://pynq.readthedocs.io/) | Ready-made board-specific audio notebook and overlay not yet verified |
| HW-06 | [Sobel Edge Detection and Image Compositing — complete project](https://github.com/Adhiraj4/Sobel-Edge-detection-and-inference-based-Image-Compositing-using-Vitis-HLS-for-Pynq-Z2-FPGA) | Concrete PYNQ-Z2 Sobel project with notebook and precompiled overlay |
| HW-07 | [Pieter Berteloot — Sharpening project](https://github.com/Pieter-Berteloot/PYNQ_Projects/tree/master/Sharpening) | A specific example exists, but programmable coefficient support is unverified |
| HW-09 | [Lab03 — XADC data logging and monitoring](../../Lab03/README.md) | Available laboratory notebook (PS measurements), hardware acceleration needs a verified compatible path |

## General Project Guidelines

Students primarily **reproduce, explain and extend an existing working project**, using its notebook and precompiled overlay. They write Python/Jupyter notebook code only, using existing Lab06–Lab08 overlays or compatible public downloadable overlays. No RTL, HLS, Vivado, IP generation or new bitstream generation is part of the assignment.

Every notebook must demonstrate a real PL operation, document the selected board and the matching .bit/.hwh files, explain the ARM–FPGA interaction, compare results to software, and show practical outputs. If a compatible ready-made overlay is not found, the project is **conditional** and cannot yet be allocated as a co-design FPGA project.

### Public overlay examples

- [Lab06 MAC overlay](../Lab06/README.md) — Zybo Legacy
- [Lab07 DMA threshold overlay](../Lab07/README.md) — Zybo Legacy
- [Lab08 BNN overlay](../Lab08/README.md) — Zybo Legacy
- [PYNQ-Z2 FIR with notebook and precompiled .bit/.hwh](https://github.com/prnjl10/dma-fir-accelerator-pynq-z2) — public external example
- [PYNQ Workshop](https://github.com/Xilinx/PYNQ_Workshop) — additional notebooks and overlay concepts

Other topics (DDS, FFT, configurable convolution, RLE, QRS) require verifying a precompiled compatible overlay **before** project assignment.

## Recommended Project Schedule

| Week | Activities | Deliverable |
| --- | --- | --- |
| 1 | Obtain and verify the overlay, then reproduce the original notebook. | Working baseline |
| 2 | Develop Python controls, test data and explanations. | Improved notebook |
| 3 | Add plots, interactivity and meaningful experiments. | Practical demonstrations |
| 4 | Validate results against software, measure execution and transfer time. | Verified results |
| 5 | Complete documentation and present the notebook. | Final submission |

## Evaluation Criteria

| Criterion | Weight |
| --- | ---: |
| Functional notebook and demonstrated FPGA overlay use | 35% |
| Explanation of PS–PL operation | 25% |
| Correctness, test cases and useful comparisons | 15% |
| Documentation and reproducibility | 15% |
| Python notebook improvements and interactivity | 10% |
| **Total** | **100%** |

Maximum grades on the **1–5 scale** will be agreed after feasibility and complexity checks.

## Main Sources and Background

- [Adam Taylor — GitHub repositories](https://github.com/ATaylorCEngFIET?tab=repositories)
- [Hackster.io FPGA/Zynq projects](https://www.hackster.io/search?i=projects&q=Zynq%20FPGA)
- Xilinx DSP Primer (instructor-provided archive)
- [The Zynq Book and tutorials](https://www.zynqbook.com/)
- [PYNQ documentation](https://pynq.readthedocs.io/)
- [Course Lab06 — AXI and FPGA MAC](../Lab06/README.md)
- [Course Lab07 — AXI DMA image processing](../Lab07/README.md)
- [Course Lab08 — FPGA BNN inference](../Lab08/README.md)

The links above include **direct implementations** and **broader conceptual resources**. These are distinguished in the individual project pages; they do not imply that a ready-to-use Zybo or PYNQ-Z2 overlay is supplied for each project.
