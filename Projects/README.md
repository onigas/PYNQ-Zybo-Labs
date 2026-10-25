# Hardware–Software Co-design — FPGA Project Proposals

**Repository:** PYNQ-Zybo-Labs  
**Target platforms:** Digilent Zybo Legacy / Digilent PYNQ-Z2 (as indicated)  
**Suggested duration:** 4–5 weeks  
**Development:** Vivado 2022.2, RTL/IP/HLS, PS software in Python or C/C++

The **13 selected proposals** are listed below. Click a project title to open its individual assignment. The original HW identifiers have been retained (HW-08 was not selected).

| Code | Project title | Implementation board |
| --- | --- | --- |
| HW-01 | [Programmable Arithmetic Accelerator](Details/HW-01.md) | Zybo Legacy / PYNQ-Z2 |
| HW-02 | [DDS Waveform Generator](Details/HW-02.md) | Zybo Legacy / PYNQ-Z2 |
| HW-03 | [FIR Filter Accelerator](Details/HW-03.md) | Zybo Legacy / PYNQ-Z2 |
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

## General Project Guidelines

The aim is to practice **hardware–software co-design**: the Processing System (PS, ARM) runs a software application, while the Programmable Logic (PL, FPGA) implements a specific processing function. A Python notebook alone, or an HDL-only design without PS control/data exchange, does not satisfy the assignment.

Students **may reproduce and adapt open-source reference projects**. The contribution must be explained, the solution demonstrated, and all sources credited. A prebuilt overlay is acceptable as a starting point, but students must document its architecture and show what they configured, modified or extended.

Each project should include:

- A block diagram showing PS, PL, AXI communication and data paths.
- A software component (Python/PYNQ or C/C++) and a functional FPGA accelerator.
- An operational demonstration on **the board listed for the project**.
- Functional verification against a software reference, with at least one representative input/output example.
- Resource utilization and a performance discussion including data-transfer overhead where relevant.
- Documentation listing the required equipment, software versions, third-party code and adaptations.

**Platform note:** Zybo Legacy and PYNQ-Z2 are both Zynq-7000-based but have different board constraints, interfaces and overlay support. Board applicability in the table indicates a **feasible implementation target**, not an already-tested bitstream. Existing Zybo overlays in this repository must not be assumed to work unchanged on PYNQ-Z2.

## Recommended Project Schedule

| Week | Activities | Expected Deliverables |
| --- | --- | --- |
| 1 | Study references, define a reproducible demonstration, identify PS/PL tasks and interfaces. | Requirements, hardware/software block diagram, implementation plan |
| 2 | Implement/adapt accelerator RTL/HLS/IP and develop the PS reference application. | Hardware sources, software reference, preliminary verification |
| 3 | Integrate AXI register/DMA communication, build overlay and run on board. | First operational PS–PL prototype |
| 4 | Validate functional outputs, debug integration and measure resources/timing. | Hardware demonstration, correctness and performance results |
| 5 | Add a useful extension, finalize report and present the project. | Source repository, report and live demonstration |

For a four-week assignment, combine the final verification and presentation stages.

## Evaluation Criteria

| Criterion | Weight |
| --- | ---: |
| Functional PS–PL implementation and FPGA demonstration | 35% |
| Understanding and explanation of hardware/software partitioning and architecture | 25% |
| Verification and performance/resource evaluation | 15% |
| Technical documentation and reproducibility | 15% |
| Adaptations and useful extensions | 10% |
| **Total** | **100%** |

Maximum grades on a **1–5 scale** will be determined after each detailed project specification is reviewed. The percentage rubric assesses the quality of the selected project; reproducing reference code without understanding does not automatically earn the maximum grade.

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
