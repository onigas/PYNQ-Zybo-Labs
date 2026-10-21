# Archived GTSRB research utilities

This directory preserves **original exploratory source files** from the earlier Lab08 work. They are not imported by the current teaching notebooks and must not replace the tested ARM software model or compact FPGA overlay.

| File | Purpose | Status |
|---|---|---|
| [tools/download_assets.py](tools/download_assets.py) | Downloads and extracts the complete official GTSRB test archives and FINN model archive. | Historical; network URLs may have changed. |
| [tools/eval_qonnx_gtsrb.py](tools/eval_qonnx_gtsrb.py) | Runs a FINN/QONNX classifier on labeled GTSRB photographs, measures latency and records predictions. | Requires the full image dataset, ONNX model and compatible x86 QONNX environment; not verified here. |
| [tools/gtsrb.py](tools/gtsrb.py) | Loads the complete test dataset, stratified sampling, RGB preprocessing and confusion matrices. | Requires all labeled photographs for its strict completeness check. |
| [tools/live_gtsrb.py](tools/live_gtsrb.py) | HSV-based red/blue sign candidate detection, region cropping and generic accelerator-call wrapper. | Experimental; expects an accelerator with an execute() method, not the tested Lab08.3 DMA API. |
| [tools/plot_results.py](tools/plot_results.py) | Summarizes predictions, times and confusion matrix, and displays incorrect classifications. | Reusable when predictions.csv has been generated. |
| [tools/smoke_test.py](tools/smoke_test.py) | Self-contained loader and sampling tests on synthetic files. | Synthetic data is used only to test utility behavior, never to claim model accuracy. |

## Path and environment notes

These Python scripts are preserved unchanged. Because they were relocated from Lab08/tools to Lab08/research/tools to avoid clashing with the **current** Lab08/tools/gtsrb.py, some scripts resolve defaults relative to Lab08/research instead of Lab08. Set explicit paths as needed.

For example, from the repository root:

    python3 Lab08/research/tools/download_assets.py --root Lab08 --dataset-only

The command downloads the **entire** official GTSRB test set and is **not required** for ordinary Lab08.1–Lab08.3 exercises. Do not invoke it on the Zybo SD card without checking available space.

QONNX evaluation is intended for an x86 development computer with FINN/QONNX and the full GTSRB test archive. The five photographs bundled for the teaching exercises are intentionally insufficient for full-dataset evaluation.

For exploratory XC7Z010 FINN build configurations see [../hardware/](../hardware/).
