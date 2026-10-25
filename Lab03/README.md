# Lab 03 — XADC and System Monitoring

**Board:** Zybo Legacy with the course PYNQ 3.0.1 image. These experiments acquire information via Linux IIO on the ARM Processing System; **no custom FPGA accelerator is required**.

## Existing Notebooks

| Notebook | Purpose |
| --- | --- |
| [Lab03.1 — XADC Temperature](Lab03.1_XADC_Temperature.ipynb) | Read the die temperature |
| [Lab03.2 — XADC Voltages](Lab03.2_XADC_Voltages.ipynb) | Read internal supply voltages |
| [Lab03.3 — XADC Data Logging](Lab03.3_XADC_Data_Logging.ipynb) | Record samples, visualize and export CSV |
| [Lab03.4 — XADC Thermal Response](Lab03.4_XADC_Thermal_Response.ipynb) | Observe response to a controlled CPU load |
| [Lab03.5 — Thermal Alarm](Lab03.5_Thermal_Alarm_Automatic_Protection.ipynb) | Explore conservative thresholding/hysteresis and workload shutdown |
| [Lab03.6 — Integrated System Monitor](Lab03.6_Integrated_XADC_System_Monitor.ipynb) | Combine readings and alerts |

## Reproduction and Notebook Extension

**Reproduce:** Run notebooks 03.1 through 03.6 on the documented board/image, preserve original measurements and explain temperature, voltage and status readings.

**Suggested notebook-only extension:** Add a dashboard showing recorded temperature and voltage with user-selected thresholds, a visible alert timeline and CSV export. The values must come from the real available IIO sensors, not invented data.

**Implementation boundary:** These are **ARM/Linux measurement and monitoring experiments**, not PL hardware accelerators. The thermal-protection experiment is a teaching model, not hardware overtemperature protection. No Vivado, HDL or new overlay generation is required.
