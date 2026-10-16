# Lab08 — Pretrained BNN traffic-sign recognition

**Board:** Digilent Zybo Legacy (XC7Z010), **PYNQ:** 3.0.1, **runtime:** ARM software. Both notebooks were tested on the real board.

## Notebooks

| Notebook | Purpose | Board verification |
|---|---|---|
| [Lab08.1_GTSRB_Real_Dataset.ipynb](notebooks/Lab08.1_GTSRB_Real_Dataset.ipynb) | Inspect official GTSRB CSV (12,630 annotations), 43 sign classes, images and 32×32 RGB resizing | Verified; `np.bincount` uses `int32` for ARMv7 compatibility |
| [Lab08.2_BNN_PYNQ_ARM_Inference.ipynb](notebooks/Lab08.2_BNN_PYNQ_ARM_Inference.ipynb) | Load original pretrained CNV-W1A1 weights from [BNN-PYNQ](https://github.com/onigas/BNN-PYNQ), classify one of five official images, run five-image benchmark | **5/5 correctly classified**; mean ARM inference **1.587 s/image**, 0.630 images/s (library-reported) |

**Important:** 5/5 is accuracy on **five selected images**, *not* accuracy on the full GTSRB test set. The neural network runs on ARM in software; **neither notebook loads an FPGA bitstream**. FPGA BNN acceleration on XC7Z010 has not yet been implemented or benchmarked.

## Prepare test data on Zybo

Preserve this directory structure:

```text
Lab08/
├── README.md
├── notebooks/
│   ├── Lab08.1_GTSRB_Real_Dataset.ipynb
│   └── Lab08.2_BNN_PYNQ_ARM_Inference.ipynb
├── tools/
│   └── gtsrb.py
└── data/gtsrb/
    ├── GT-final_test.csv
    └── GTSRB/Final_Test/Images/00105.ppm
```

The last two files are **not included in Git**. Download the original [GTSRB dataset](https://benchmark.ini.rub.de/gtsrb_dataset.html) and copy **`GT-final_test.csv`** (the semicolon-separated official ground-truth file) and **`00105.ppm`** (from the official test-images archive) into the locations shown. Only one photograph is needed to start Lab08.1. If the board already has these files from earlier experiments, no action is needed.

## Run Lab08.2

1. Start Jupyter on Zybo and open `Lab08/notebooks/Lab08.2_BNN_PYNQ_ARM_Inference.ipynb`.
2. Run sections 1–3. Section 2 downloads the original **32-bit ARM software library** and **179 parameter/class-label files** from a pinned `onigas/BNN-PYNQ` commit into `Lab08/assets/bnn_pynq_sw/`. Previously downloaded files are reused and checked. The notebook also documents a manual offline ZIP transfer.
3. Run section 4. It selects five images with real labels from the official CSV (classes 4, 14, 1, 25, 33). If needed, it temporarily downloads the official **~84 MB GTSRB test-images archive**, extracts only the missing photographs, then removes the temporary archive. Have sufficient SD-card space and internet access or transfer the images manually.
4. In section 5, change `IMAGE_INDEX = 0` to any integer from `0` to `4`. Run sections 5–6 to classify the selected image.
5. Run section 7 to evaluate all five images in one isolated ARM process and report sample accuracy and average software inference time.

**Dependencies:** Python 3.10, NumPy, OpenCV, Pillow, Matplotlib (available in the tested PYNQ 3.0.1 image). The historical BNN library is executed in a subprocess to avoid crashing the Jupyter kernel if incompatible. Do not install the original BNN-PYNQ package: its setup script explicitly supports PYNQ-Z1/Z2 and Ultra96, not Zybo.

## Source and provenance

The CPU classifier and pretrained road-sign parameters come from [onigas/BNN-PYNQ](https://github.com/onigas/BNN-PYNQ), a fork of Xilinx BNN-PYNQ. Runtime source snapshot: `d39c1c75403db571f54dd0f0cf27ae5104ac968e`. The original GTSRB images and CSV are used for evaluation. The `.so`, large test-data archive, per-image CIFAR files, and trained parameter binaries are excluded from the lab repository and downloaded on first use.

The original PYNQ-Z2 FPGA overlay is **incompatible** with Zybo XC7Z010 and is not used. Hardware design work is a future step, not part of these two verified notebooks.
