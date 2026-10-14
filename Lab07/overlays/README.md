# Lab07 FPGA overlay for original Zybo

The pair `lab07.bit` and `lab07.hwh` (generated with Vivado 2022.2 for Zynq-7010) is used by Lab07.2 and Lab07.3. The metadata includes `axi_dma_0`, `threshold_axis_0` and `threshold_gpio`.

**Published and verified:** Both hardware files are present in this directory on the main branch. Their Git blob IDs were compared against the instructor-supplied release archive and match exactly. No Vivado compilation is required to run Lab07.2 and Lab07.3 on the supported Zybo legacy board.

SHA-256 from the verified local files:

| File | SHA-256 |
|---|---|
| `lab07.bit` | `8a639248d622e8973f28277be6850c8bc18f9e399fff9f4bb7c425a533835292` |
| `lab07.hwh` | `87bfb6eb9d29c877b17c956770504939e9072dbdbc5a10cace1d933098a90fad` |

Keep bitstream and metadata as a matched pair. They must be stored in `Lab07/overlays/` when running the notebooks. Source RTL and the project builder are in `../hardware/`.
