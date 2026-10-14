# Lab07 – FPGA-Accelerated Image Thresholding with AXI DMA

**Platform:** original Digilent Zybo (Zynq-7010), PYNQ 3.0.1, Vivado 2022.2 and optional Logitech C270 webcam.

This follows Lab06: rather than one AXI register transaction per pixel, the accelerator transfers a complete grayscale frame through **AXI DMA** and thresholds **four pixels per accepted 100 MHz clock beat**.

## Lab07 notebooks

| Notebook | Subject |
|---|---|
| [07.1 — From image pixels to AXI-Stream](notebooks/Lab07.1_Image_Threshold_Fundamentals.ipynb) | Grayscale images, labeled 32-pixel grid, selecting and displaying a ROI, intensity histogram, binary masks, AXI byte packing and ideal FPGA throughput |
| [07.2 — AXI DMA threshold accelerator](notebooks/Lab07.2_AXIDMA_Threshold_Accelerator.ipynb) | Transfer to FPGA and back; validate full image against NumPy; inspect threshold and test 256 intensities |
| [07.3 — Camera and performance benchmark](notebooks/Lab07.3_Real_Images_and_Benchmark.ipynb) | Compare software and hardware performance; selected-color demonstration using FPGA saturation threshold and ARM hue masking |

Each code cell has explanatory Markdown. The course distinguishes **ideal computation time** from measured **end-to-end PS–PL time**. A fast four-lane hardware implementation does not automatically outperform vectorized NumPy/OpenCV.

## Source code

- [AXI-Stream RTL](hardware/rtl/threshold_axis.v) and [testbench](hardware/rtl/tb_threshold_axis.v)
- [Vivado Tcl project builder](hardware/build_lab07.tcl) for the original Zybo Z-7010
- [AXI DMA Python driver](tools/dma_threshold.py), with no software fallback
- [Hardware design notes](hardware/README.md)
- [Reference-image metadata](images/README.md)

## Student installation

Download the repository as a ZIP, extract it, and copy the complete `Lab07/` directory to the Zybo Jupyter workspace. **Vivado is not needed for normal notebook execution.** Keep this structure:

```text
Lab07/
├── notebooks/
├── images/
│   ├── scene_256.png
│   └── scene_grid_256.png
├── tools/dma_threshold.py
└── overlays/
    ├── lab07.bit
    └── lab07.hwh
```

The prebuilt images and matching hardware pair are included in this repository: notebook 07.1 uses the images, while 07.2 and 07.3 also load the FPGA files. Place the directories in the same Lab07 root and launch the notebooks **from** `Lab07/notebooks/` to preserve relative paths.

## Hardware verification and timing

The instructor reported successful execution on actual Zybo legacy hardware of 07.1 (expanded revision), 07.2 (AXI DMA bit-exact checks) and 07.3 (performance test and corrected color detection). The published RTL must be checked against the exact instructor-provided hardware overlay when rebuilding.

A host-call measurement includes Python, contiguous buffers, DDR, the DMA transaction and returned results, not just the comparator delay. Also note that only the saturation threshold is computed in FPGA in the final webcam example; HSV conversion, hue filtering, morphology and contours remain on ARM.

**Publication complete:** All three notebooks, both reference images, the matching prebuilt `lab07.bit` / `lab07.hwh` pair, RTL sources, testbench, Vivado build script and AXI DMA driver are published in this repository. The binary files and PNG images were compared with the validated release archive and match byte for byte (Git blob identifiers). Students do not need Vivado to execute the notebooks.
