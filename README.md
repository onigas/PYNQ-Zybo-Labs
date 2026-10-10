# PYNQ-Zybo-Labs

Laboratory exercises for **PYNQ 3.0.1** on the **Digilent Zybo legacy (Zynq-7000)** board.

The notebooks introduce control of the on-board LEDs, switches and push buttons from Python, followed by timing, software-PWM, XADC-based system monitoring, and OpenCV-based real-time computer vision.

## Requirements

- Digilent Zybo legacy board
- SD card with PYNQ 3.0.1 for the Digilent Zybo legacy board
- the `base.bit` overlay supplied with the Zybo PYNQ image
- Ethernet connection between the computer and the board
- a web browser for the Jupyter interface
- Logitech C270 USB webcam for Lab 04

## PYNQ image

This repository was tested with the following PYNQ 3.0.1 image for the Digilent Zybo legacy board:

- Repository: https://github.com/nick-petrovsky/PYNQ-ZYBO
- Image file: `Zybo-3.0.1-fix-boot-bin-fix-havege.img.xz`

Write the image to the SD card using a raw disk imaging tool such as Win32 Disk Imager.

## Laboratory notebooks

### Lab 0 — Getting Started with PYNQ

[Open Lab 0](Lab0/README.md): PYNQ and Zynq concepts, development boards, Jupyter/JupyterLab, board connection and a first Python notebook.

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

### Lab 03 — XADC and system monitoring

| Notebook | Topic |
|---|---|
| [Lab03.1_XADC_Temperature.ipynb](Lab03/Lab03.1_XADC_Temperature.ipynb) | Zynq die-temperature measurement through Linux IIO |
| [Lab03.2_XADC_Voltages.ipynb](Lab03/Lab03.2_XADC_Voltages.ipynb) | Internal XADC supply-voltage monitoring |
| [Lab03.3_XADC_Data_Logging.ipynb](Lab03/Lab03.3_XADC_Data_Logging.ipynb) | Periodic sampling, statistics, plotting and CSV logging |
| [Lab03.4_XADC_Thermal_Response.ipynb](Lab03/Lab03.4_XADC_Thermal_Response.ipynb) | Die-temperature response under controlled CPU load |
| [Lab03.5_Thermal_Alarm_Automatic_Protection.ipynb](Lab03/Lab03.5_Thermal_Alarm_Automatic_Protection.ipynb) | Thermal warning, hysteresis and automatic workload shutdown |
| [Lab03.6_Integrated_XADC_System_Monitor.ipynb](Lab03/Lab03.6_Integrated_XADC_System_Monitor.ipynb) | Integrated XADC/GPIO monitoring assignment and optional CSV logger |

The XADC experiments use the Linux Industrial I/O interface provided by the tested PYNQ image. They do not require an AXI XADC IP block in `base.bit`.

Lab03.5 implements a deliberately conservative **software** thermal-protection experiment. It does not attempt to trigger the Zynq hardware over-temperature shutdown.

### Lab 04 — OpenCV and USB webcam color detection

[Open Lab 04](Lab04/README.md): Zybo Legacy with Logitech C270; image basics, grid-guided ROI, camera acquisition, red-marker detection and simultaneous RGB masks.

| Notebook | Topic |
|---|---|
| [Lab04.1_OpenCV_Image_Basics.ipynb](Lab04/Lab04.1_OpenCV_Image_Basics.ipynb) | Synthetic scene, BGR/RGB, grayscale and grid-selected ROI |
| [Lab04.2_USB_Webcam.ipynb](Lab04/Lab04.2_USB_Webcam.ipynb) | Logitech C270 capture with safe release |
| [Lab04.3_HSV_and_Color_Masks.ipynb](Lab04/Lab04.3_HSV_and_Color_Masks.ipynb) | Combined red-marker and simultaneous RED/GREEN/BLUE segmentation |
| [Lab04.4_Real_Time_Color_Detection.ipynb](Lab04/Lab04.4_Real_Time_Color_Detection.ipynb) | Contours, centroid, region area and successive-frame LEFT/CENTER/RIGHT/LOST tracking |
| [Lab04.5_Vision_Controlled_Zybo_LEDs.ipynb](Lab04/Lab04.5_Vision_Controlled_Zybo_LEDs.ipynb) | Camera-controlled LD0–LD3, with LEFT/CENTER/RIGHT/LOST states |

Lab04 now uses five notebooks. Lab04.3 combines red-marker and RGB color detection, Lab04.4 tracks the selected color, and Lab04.5 adds LED feedback.

### Lab 05 — Traffic Sign Recognition (OpenCV)

[Open Lab 05](Lab05/README.md): detection and classification of traffic signs from static images, including HSV segmentation, contour analysis, shape detection and rule-based recognition. No webcam or FPGA overlay is required.

| Notebook | Topic |
|---|---|
| [Lab05.1_Traffic_Sign_Color_Segmentation.ipynb](Lab05/Lab05.1_Traffic_Sign_Color_Segmentation.ipynb) | HSV red/blue segmentation and masks |
| [Lab05.2_Traffic_Sign_Shape_Detection.ipynb](Lab05/Lab05.2_Traffic_Sign_Shape_Detection.ipynb) | Contours, candidate bounding boxes and shapes |
| [Lab05.3_Traffic_Sign_Recognition.ipynb](Lab05/Lab05.3_Traffic_Sign_Recognition.ipynb) | Rule-based classification and tests on additional scenes |

Lab05 includes four synthetic images in `Lab05/images/`. Each code cell is preceded by a purpose statement and the pipeline includes visual checkpoints.

### Lab 06 — Introduction to Hardware Acceleration

[Open Lab 06](Lab06/README.md): PS–PL architecture, AXI register access, custom multiply-accumulate FPGA accelerator and batch-MAC performance analysis.

| Notebook | Topic |
|---|---|
| [Lab06.1_PS_PL_Architecture.ipynb](Lab06/notebooks/Lab06.1_PS_PL_Architecture.ipynb) | Explore PS/PL, AXI peripherals and IP metadata |
| [Lab06.2_AXI_Register_Access.ipynb](Lab06/notebooks/Lab06.2_AXI_Register_Access.ipynb) | Low-level MMIO access to LED GPIO registers |
| [Lab06.3_Custom_Hardware_Accelerator.ipynb](Lab06/notebooks/Lab06.3_Custom_Hardware_Accelerator.ipynb) | FPGA MAC accelerator: A×B+C |
| [Lab06.4_ARM_vs_FPGA_Performance.ipynb](Lab06/notebooks/Lab06.4_ARM_vs_FPGA_Performance.ipynb) | Single-MAC overhead versus batch-MAC and FPGA cycle count |

The Lab06 directory includes **two ready-to-use, verified `.bit`/`.hwh` FPGA overlay pairs** in [Lab06/overlays](Lab06/overlays), plus Vivado 2022.2 Tcl build scripts, Verilog RTL and testbenches for rebuilding. **Students do not need Vivado** to run the notebooks; preserve the Lab06 directory structure when uploading to Zybo. Lab06.4 explains that the reported speedup is relative to a **Python loop**, not an optimized ARM implementation.

## Download and use

1. Select **Code → Download ZIP** on the repository page.
2. Extract the archive on your computer.
3. In the Zybo Jupyter interface, create or open a working directory.
4. Upload the required `.ipynb` files.
5. Open the notebooks and complete them in numerical order.

Some exercises contain continuous loops or background worker processes. Use **Kernel → Interrupt** in Jupyter when instructed to stop execution. Always leave the on-board LEDs switched off after an interrupted GPIO experiment.

## Repository structure

```text
PYNQ-Zybo-Labs/
├── Lab0/
│   ├── README.md
│   └── images/
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
├── Lab03/
│   ├── Lab03.1_XADC_Temperature.ipynb
│   ├── Lab03.2_XADC_Voltages.ipynb
│   ├── Lab03.3_XADC_Data_Logging.ipynb
│   ├── Lab03.4_XADC_Thermal_Response.ipynb
│   ├── Lab03.5_Thermal_Alarm_Automatic_Protection.ipynb
│   └── Lab03.6_Integrated_XADC_System_Monitor.ipynb
├── Lab04/
│   ├── README.md
│   ├── Lab04.1_OpenCV_Image_Basics.ipynb
│   ├── Lab04.2_USB_Webcam.ipynb
│   ├── Lab04.3_HSV_and_Color_Masks.ipynb
│   ├── Lab04.4_Real_Time_Color_Detection.ipynb
│   ├── Lab04.5_Vision_Controlled_Zybo_LEDs.ipynb
│   └── images/
├── Lab05/
│   ├── README.md
│   ├── Lab05.1_Traffic_Sign_Color_Segmentation.ipynb
│   ├── Lab05.2_Traffic_Sign_Shape_Detection.ipynb
│   ├── Lab05.3_Traffic_Sign_Recognition.ipynb
│   └── images/
├── Lab06/
│   ├── README.md
│   ├── notebooks/
│   │   ├── Lab06.1_PS_PL_Architecture.ipynb
│   │   ├── Lab06.2_AXI_Register_Access.ipynb
│   │   ├── Lab06.3_Custom_Hardware_Accelerator.ipynb
│   │   └── Lab06.4_ARM_vs_FPGA_Performance.ipynb
│   ├── overlays/
│   │   ├── lab06.bit
│   │   ├── lab06.hwh
│   │   ├── lab06_batch.bit
│   │   ├── lab06_batch.hwh
│   │   └── README.md
│   └── hardware/
│       ├── README.md
│       ├── build_lab06.tcl
│       ├── build_lab06_batch.tcl
│       └── rtl/
├── tools/
│   └── xadc_iio_test.py
└── README.md
```
