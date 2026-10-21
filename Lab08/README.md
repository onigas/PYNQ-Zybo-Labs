# Lab08 — GTSRB traffic-sign recognition: dataset, ARM BNN and FPGA BNN

**Platform:** Digilent Zybo Legacy (XC7Z010), PYNQ 3.0.1.

## Published laboratory notebooks

| Notebook | Experiment | Previously verified on real Zybo |
|---|---|---|
| [Lab08.1 — GTSRB Dataset](notebooks/Lab08.1_GTSRB_Real_Dataset.ipynb) | Analyze the official GTSRB test CSV (12,630 labels), 43 classes, RGB images and resizing | Runs on ARM |
| [Lab08.2 — Pretrained BNN on ARM](notebooks/Lab08.2_BNN_PYNQ_ARM_Inference.ipynb) | Original CNV-W1A1 model from [BNN-PYNQ](https://github.com/onigas/BNN-PYNQ), five selectable official GTSRB images | **5/5** correct; average library-reported **1.587 s/image** |
| [Lab08.3 — Compact BNN on FPGA](notebooks/Lab08.3_BNN_FPGA_Inference_GTSRB.ipynb) | Real compact BNN overlay using AXI DMA, official traffic-sign images and optional Logitech C270 camera | **13/20** correct on selected GTSRB Test images; average end-to-end **23.15 ms/image** |

**Numbering:** the FPGA experiment was initially tested and saved as **Lab08.4**. It has been renumbered **Lab08.3** to avoid a gap. The abandoned, resource-exceeding **full nine-layer CNV HLS design** is NOT part of Lab08.

**Do not calculate a same-model acceleration factor:** Lab08.2 (ARM CNV-W1A1) and Lab08.3 (compact FPGA BNN) use **different classifiers** and **different timing boundaries**. Their timings illustrate the respective implementations only. The selected sets of five and twenty test photographs do not establish full GTSRB accuracy.

## Required files and directory structure

```text
Lab08/
├── README.md
├── notebooks/
│   ├── Lab08.1_GTSRB_Real_Dataset.ipynb
│   ├── Lab08.2_BNN_PYNQ_ARM_Inference.ipynb
│   ├── Lab08.3_BNN_FPGA_Inference_GTSRB.ipynb
│   ├── BATCH20_CELL.py
│   └── gtsrb_batch20_inputs.npz               <-- original 20-image FPGA test
├── display/                                  <-- 20 SVG illustrations, manifest.json, index.html
├── overlays/
│   ├── compact_gtsrb.bit                      <-- original XC7Z010 overlay
│   └── compact_gtsrb.hwh                      <-- corresponding Vivado hardware handoff
├── evidence/
│   └── FPGA_VALIDATION.md                     <-- saved results from the original Zybo run
├── tools/
│   └── gtsrb.py
└── data/gtsrb/
    ├── GT-final_test.csv                     <-- used by Lab08.1; not needed for 08.3
    └── GTSRB/Final_Test/Images/
        └── 00105.ppm                          <-- official GTSRB test image
```

**Binary artifact status:** all three original files are committed to `main`: [`compact_gtsrb.bit`](overlays/compact_gtsrb.bit), [`compact_gtsrb.hwh`](overlays/compact_gtsrb.hwh), and [`gtsrb_batch20_inputs.npz`](notebooks/gtsrb_batch20_inputs.npz). Their sizes and reference SHA-256 checksums are listed in [evidence/FPGA_VALIDATION.md](evidence/FPGA_VALIDATION.md). Download the complete repository to preserve the directory structure. **Never replace the FPGA bitstream with the abandoned full-CNV project's output.**

## Lab08.1 — Prepare GTSRB data

The official `GT-final_test.csv` is a semicolon-separated dataset with 12,630 image labels. Download it together with `00105.ppm` from the [original GTSRB dataset](https://benchmark.ini.rub.de/gtsrb_dataset.html) and copy both to the locations shown. If the board already has the data from earlier experiments, reuse it. The notebooks do not require copying every one of the 12,630 photographs.

## Lab08.2 — Pretrained ARM inference

Open the notebook in Jupyter. Its asset download cell retrieves one original 32-bit ARM shared library and 179 parameter/label files from the pinned original BNN-PYNQ source commit `d39c1c75403db571f54dd0f0cf27ae5104ac968e` (offline ZIP procedure is provided). It then selects five official GTSRB Test images and can download the missing four photos from the official test archive. Classify one example by changing `IMAGE_INDEX` from 0 to 4; evaluate all five with the included batch cell. No FPGA is programmed in Lab08.2.

## Traffic-sign display for camera experiments

The [display/](display/) directory provides **20 scalable SVG traffic-sign illustrations** and an offline [interactive HTML viewer](display/index.html) with Previous/Next navigation. The same viewer is available inside `Lab08.3` through Jupyter widgets. Copy the **complete Lab08 directory**, including `display/`, to Zybo to use the notebook viewer. Open `display/index.html` on a computer or phone after downloading the folder to navigate the signs.

These SVG files are **schematic reference illustrations for the 20 GTSRB classes**, not photographs from the GTSRB dataset and not the exact 20 images used in the FPGA benchmark. They are suitable for showing signs to a webcam, but real-camera inference may differ from the recorded 13/20 offline benchmark. In the camera experiment, the sign should occupy most of the centered crop; the existing camera cell classifies only one captured frame, not a continuous video stream.

## Lab08.3 — Real compact FPGA inference

The original tested code uses `pynq.Overlay`, `allocate`, `axi_dma_0`, and two DMA buffers. The **first code cell programs the FPGA** with `compact_gtsrb.bit`. The single-image test selects a labeled image from the bundled `notebooks/gtsrb_batch20_inputs.npz` archive and does not require an internet connection, the official CSV, or external photographs. The 20-image test calls [BATCH20_CELL.py](notebooks/BATCH20_CELL.py) using the same archive. The optional camera cell captures one frame from the Logitech C270.

The published notebook's single-image section uses the same bundled preprocessed inputs as the 20-image test to avoid network requirements. This revised section has not yet been rerun on the physical board. No hardware, FPGA inference function or previously tested image bytes have been intentionally altered. Full Vivado build sources for this compact bitstream have not been recovered.

**Prior verified result details:** [FPGA_VALIDATION.md](evidence/FPGA_VALIDATION.md).

## Limitations and provenance

- GTSRB Test accuracy on 5 or 20 selected images is not full-dataset accuracy.
- FPGA output consists of 44 signed int16 scores; class 43 is padding and must be treated as invalid.
- The reported 23.15 ms/image is Python + cache + DMA + FPGA end-to-end time, not hardware core latency.
- On camera: one inference was obtained, not a verified correctly recognized sign.
- No FINN/QONNX development environment is required to **run** these experiments on Zybo.
