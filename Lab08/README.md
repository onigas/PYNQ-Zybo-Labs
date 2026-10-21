# Lab08 — GTSRB traffic-sign recognition: dataset, ARM BNN and FPGA BNN

**Platform:** Digilent Zybo Legacy (XC7Z010), PYNQ 3.0.1.

> **Offline-ready resources:** the original GTSRB ground-truth CSV, five test photographs, and the pretrained ARM BNN software/parameters are committed to `main`. Clone or download the complete repository to run Lab08.1 and Lab08.2 without additional downloads.

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
├── data/gtsrb/
│   ├── GT-final_test.csv                     <-- 12,630 genuine test labels
│   └── GTSRB/
│       ├── Readme-Images-Final-test.txt      <-- original dataset description
│       └── Final_Test/Images/
│           ├── 00001.ppm                      <-- original test photos for ARM
│           ├── 00003.ppm
│           ├── 00008.ppm
│           ├── 00093.ppm
│           └── 00105.ppm
├── assets/bnn_pynq_sw/
│   ├── python_sw-cnvW1A1-pynqZ1-Z2.so        <-- original 32-bit ARM CNV software
│   └── params/                               <-- 178 weight/threshold bins + classes.txt
├── hardware/                                 <-- preserved experimental FINN Z7010 configs
└── research/tools/                           <-- archived source utilities, not current notebook API
```

**Binary artifact status:** all three original files are committed to `main`: [`compact_gtsrb.bit`](overlays/compact_gtsrb.bit), [`compact_gtsrb.hwh`](overlays/compact_gtsrb.hwh), and [`gtsrb_batch20_inputs.npz`](notebooks/gtsrb_batch20_inputs.npz). Their sizes and reference SHA-256 checksums are listed in [evidence/FPGA_VALIDATION.md](evidence/FPGA_VALIDATION.md). Download the complete repository to preserve the directory structure. **Never replace the FPGA bitstream with the abandoned full-CNV project's output.**

## Lab08.1 — Prepare GTSRB data

The original `GT-final_test.csv` is a semicolon-separated file containing 12,630 image labels. The five real test photographs used by the ARM experiment are `00105.ppm`, `00093.ppm`, `00001.ppm`, `00008.ppm` and `00003.ppm`. They come from the official [GTSRB dataset](https://benchmark.ini.rub.de/gtsrb_dataset.html) and correspond to five different classes. The teaching notebooks require only these five photographs, **not** the complete 12,630-image archive.

## Lab08.2 — Pretrained ARM inference

Open the notebook in Jupyter. The original 32-bit ARM shared library, 178 trained binary parameter files and `classes.txt` belong in `assets/bnn_pynq_sw/`. Their source is the pinned BNN-PYNQ commit `d39c1c75403db571f54dd0f0cf27ae5104ac968e`. The notebook now defaults to **offline operation**, with `DOWNLOAD_ASSETS = False` and `DOWNLOAD_MISSING_IMAGES = False`. Enable one of the recovery options only if the relevant original files are missing. Classify a selected photograph by changing `IMAGE_INDEX` from 0 to 4, or test all five. No FPGA is programmed in Lab08.2.

## Traffic-sign display for camera experiments

The [display/](display/) directory provides **20 scalable SVG traffic-sign illustrations** and an offline [interactive HTML viewer](display/index.html) with Previous/Next navigation. The notebook `Lab08.3` provides a Jupyter viewer alongside a **Capture & classify** button: select a sign, capture a new Logitech C270 frame, and display the FPGA classification and time next to the reference. Repeated captures do not require rerunning the cell. **Section 8** benchmarks 20 consecutive Logitech C270 frames, separately measuring capture, ARM preprocessing, FPGA inference calls and end-to-end throughput. It automatically displays an English interpretation of the measured times, stage percentages, effective FPS and example distance traveled between frames at 130 km/h. The camera is released after each Section 7 capture using `finally: cap.release()`; no manual Release button is required. It reports observed processing rate, not validated traffic-sign detection latency or vehicle-level real-time performance. Copy the **complete Lab08 directory**, including `display/`, to Zybo to use the notebook viewer. Open `display/index.html` on a computer or phone after downloading the folder to navigate the signs.

These SVG files are **schematic reference illustrations for the 20 GTSRB classes**, not photographs from the GTSRB dataset and not the exact 20 images used in the FPGA benchmark. They are suitable for showing signs to a webcam, but real-camera inference may differ from the recorded 13/20 offline benchmark. In the camera experiment, the sign should occupy most of the centered crop. Each click captures one new frame; this is not a continuous video stream.

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

## Preserved development and research materials

- [hardware/](hardware/) preserves the original XC7Z010 FINN feasibility script, folding configuration and HLS/RTL specialization preferences. These files are **experimental and unvalidated**, not the bitstream or synthesis project used in the successful compact FPGA demonstration. They are retained for possible future development.
- [research/](research/) preserves six exact original GTSRB helper scripts for dataset download, full-set QONNX evaluation, stratified sampling, HSV candidate detection, prediction visualization and smoke tests. They are intentionally separate from the current `tools/gtsrb.py` because the historical helper uses a different interface.
- The official GTSRB CSV and five teaching images, and the original BNN-PYNQ ARM software library and trained parameters, are recovery artifacts extracted from a previously tested Zybo installation. Do **not** substitute newly generated weights, unrelated traffic-sign images, or the failed full-CNV hardware design.
