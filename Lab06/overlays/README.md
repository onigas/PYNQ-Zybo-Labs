# Prebuilt PYNQ overlays for Zybo legacy

The paired FPGA files belong in this directory:

- `lab06.bit` + `lab06.hwh`: single-operation MAC (`mac8_0`)
- `lab06_batch.bit` + `lab06_batch.hwh`: batch MAC with cycle counter (`batch_mac_0`)

Both bitstreams were provided from Vivado **2022.2** for device **7z010clg400**. Their metadata contains the expected AXI GPIO blocks.

**Status:** All four prebuilt FPGA files are committed in this directory. The uploaded Git blobs have been compared against the original instructor-provided files and match byte for byte (SHA-1 Git blob IDs). Students can use them directly without installing Vivado. Source code and Tcl build scripts are available in `../hardware/`. Notebooks 06.3 and 06.4 locate the matching `.bit`/`.hwh` pairs automatically.

## Published binary integrity: SHA-256

| File | SHA-256 |
|---|---|
| `lab06.bit` | `a7d8b3ce1aba9d0bafd2fefd542e7fde1aaf247f2ef35f7ecb1e7ee8203c637f` |
| `lab06.hwh` | `03d6197072373ece86fb14cbb267ec4a47c307b6ae02f2e44c129c29be60d462` |
| `lab06_batch.bit` | `442900538b9f0b7bbbf5112de34dee831ad7e32e34a47770b3fccc9c71444df5` |
| `lab06_batch.hwh` | `4c9d84bc214e055cb36f6369dfeb8cfbd45381ace49a910a35299d140e57a050` |

Place these files in this folder, or copy matching pairs beside each notebook for backward compatibility. Do not mix `.bit` and `.hwh` from different builds.
