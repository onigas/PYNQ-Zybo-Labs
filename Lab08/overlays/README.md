# Compact GTSRB FPGA overlay (Lab08.3)

Place the **original**, previously tested Zybo Legacy XC7Z010 overlay files here:

- `compact_gtsrb.bit` (2,083,852 bytes)
- `compact_gtsrb.hwh` (579,702 bytes)

They must have identical base names so that `pynq.Overlay("../overlays/compact_gtsrb.bit")` can load the HWH metadata automatically.

The files were provided and verified locally and are included in the archive `Lab08.4_Zybo_Recovered.zip`, but were **not transferred to GitHub through the connector**. Do not use the unsuccessful nine-layer CNV HLS project's bitstream. To finish GitHub packaging, upload these two binary files directly to this directory via GitHub's **Add file → Upload files** interface. Reference SHA-256 hashes are documented in [../evidence/FPGA_VALIDATION.md](../evidence/FPGA_VALIDATION.md).

Hardware input: 3072 bytes of interleaved RGB8 per 32×32 image; hardware output: 88 bytes containing 44 signed 16-bit scores, class 43 unused padding. AXI DMA controller: `axi_dma_0`.
