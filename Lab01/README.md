# Lab 01 — Basic GPIO

This laboratory introduces the PYNQ `base.bit` overlay and the on-board GPIO devices of the Digilent Zybo legacy board.

Complete the notebooks in the following order:

| Notebook | Main activity |
|---|---|
| [Lab01.1_LED.ipynb](Lab01.1_LED.ipynb) | Control individual on-board LEDs |
| [Lab01.2_Switch_LED.ipynb](Lab01.2_Switch_LED.ipynb) | Read switches and map their states to LEDs |
| [Lab01.3_Buttons.ipynb](Lab01.3_Buttons.ipynb) | Read the four push buttons |
| [Lab01.4_Button_Counter.ipynb](Lab01.4_Button_Counter.ipynb) | Implement a four-bit button-controlled counter |
| [Lab01.5_Integrated_GPIO_Project.ipynb](Lab01.5_Integrated_GPIO_Project.ipynb) | Combine LEDs, switches and buttons in an individual mini-project |

Required hardware: **Zybo legacy only**. No external components or sensors are needed.

## Reproduction and Notebook Extension

**Existing starting point:** [Lab01.1–Lab01.5 notebook sequence](README.md).

**Reproduce:** Reproduce LED, switch, button and counter examples using the existing base overlay and the onboard GPIO.

**Suggested notebook-only extension:** Extend Lab01.5 into a simple stateful control panel that combines a selected switch mode, a button event and an LED indication; demonstrate all states.

**Implementation boundary:** Uses pre-existing GPIO logic in the base overlay; no custom accelerator. Students do not need to use Vivado, create HDL/HLS, or regenerate overlays.
