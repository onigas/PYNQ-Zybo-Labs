# FINN GTSRB feasibility configuration for Zybo Legacy (XC7Z010)

This directory preserves the exploratory configuration for porting the complete pretrained FINN GTSRB CNV-W1A1 network to the Zynq-7010. It is useful for future research, but **it is not a validated build**.

## Files

- [finn_z7010.py](finn_z7010.py): experimental FINN DataflowBuildConfig, targeting xc7z010clg400-1; requests resource estimates, stitched IP and a PYNQ driver (not a bitstream).
- [folding_z7010.json](folding_z7010.json): proposed low-parallelism PE/SIMD settings to reduce resource pressure.
- [specialize_gtsrb.json](specialize_gtsrb.json): proposed HLS/RTL implementation preferences for FINN operators.

The configuration files are preserved from the original work. They have **not** been re-run or validated against the installed FINN version; operator names, APIs and configurations may require adaptation.

## Relationship to working laboratories

- **Lab08.2:** runs the original pretrained CNV-W1A1 BNN as an ARM software library, not using these configs.
- **Lab08.3:** runs a separately developed and tested compact accelerator: [compact_gtsrb.bit](../overlays/compact_gtsrb.bit) and [compact_gtsrb.hwh](../overlays/compact_gtsrb.hwh).
- **The full nine-layer CNV FINN/HLS experiment did not yield a usable XC7Z010 accelerator.** These configs must not be presented as a replacement for the tested compact overlay.

## Possible future workflow

On a compatible x86 Linux FINN host (not Zybo ARM), obtain the pretrained model and place it at Lab08/models/cnv_1w1a_gtsrb.onnx. Examine estimated LUT, FF, BRAM and DSP use before attempting integration. The full model is not included in the teaching repository.

Source context: [Xilinx/finn-examples GTSRB](https://github.com/Xilinx/finn-examples/tree/main/build/gtsrb).

**Status:** historical research configuration; not tested. Preserve for future work.
