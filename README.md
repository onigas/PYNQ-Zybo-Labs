# PYNQ-Zybo-Labs

Laboratory exercises for **PYNQ 3.0.1** on the **Digilent Zybo legacy (Zynq-7000)** board.

The notebooks introduce control of the on-board LEDs, switches and push buttons from Python, followed by timing and software-PWM experiments.

## Requirements

- Digilent Zybo legacy board
- SD card with PYNQ 3.0.1
- the `base.bit` overlay supplied with the Zybo PYNQ image
- Ethernet connection between the computer and the board
- a web browser for the Jupyter interface

No external sensors or additional hardware are required.

## Laboratory notebooks

### Lab 01 — Basic GPIO

| Notebook | Topic |
|---|---|
| [Lab01.1_LED.ipynb](Lab01/Lab01.1_LED.ipynb) | Loading the base overlay and controlling LEDs |
| [Lab01.2_Switch_LED.ipynb](Lab01/Lab01.2_Switch_LED.ipynb) | Reading switches and driving LEDs |
| [Lab01.3_Buttons.ipynb](Lab01/Lab01.3_Buttons.ipynb) | Reading push buttons |
| [Lab01.4_Button_Counter.ipynb](Lab01/Lab01.4_Button_Counter.ipynb) | Four-bit counter controlled by push buttons |
| [Lab01.5_Integrated_GPIO_Project.ipynb](Lab01/Lab01.5_Integrated_GPIO_Project.ipynb) | Integrated GPIO mini-project and extended task |

### Lab 02 — Timing and software PWM

| Notebook | Topic |
|---|---|
| [Lab02.1_Timing.ipynb](Lab02/Lab02.1_Timing.ipynb) | Python timing and periodic signals |
| [Lab02.2_Software_PWM.ipynb](Lab02/Lab02.2_Software_PWM.ipynb) | Software PWM fundamentals |
| [Lab02.3_PWM_LED_Brightness.ipynb](Lab02/Lab02.3_PWM_LED_Brightness.ipynb) | LED brightness fading using PWM |
| [Lab02.4_Button_Controlled_PWM.ipynb](Lab02/Lab02.4_Button_Controlled_PWM.ipynb) | Button-controlled PWM |
| [Lab02.5_Dual_LED_PWM_Controller.ipynb](Lab02/Lab02.5_Dual_LED_PWM_Controller.ipynb) | Dual-LED PWM controller and timing investigation |

## Download and use

1. Select **Code → Download ZIP** on the repository page.
2. Extract the archive on your computer.
3. In the Zybo Jupyter interface, create or open a working directory.
4. Upload the required `.ipynb` files.
5. Open the notebooks and complete them in numerical order.

Some exercises contain continuous loops. Use **Kernel → Interrupt** in Jupyter when instructed to stop execution. Always leave the on-board LEDs switched off after an interrupted experiment.

## Repository structure

```text
PYNQ-Zybo-Labs/
├── Lab01/
│   ├── Lab01.1_LED.ipynb
│   ├── Lab01.2_Switch_LED.ipynb
│   ├── Lab01.3_Buttons.ipynb
│   ├── Lab01.4_Button_Counter.ipynb
│   └── Lab01.5_Integrated_GPIO_Project.ipynb
├── Lab02/
│   ├── Lab02.1_Timing.ipynb
│   ├── Lab02.2_Software_PWM.ipynb
│   ├── Lab02.3_PWM_LED_Brightness.ipynb
│   ├── Lab02.4_Button_Controlled_PWM.ipynb
│   └── Lab02.5_Dual_LED_PWM_Controller.ipynb
└── README.md
```
