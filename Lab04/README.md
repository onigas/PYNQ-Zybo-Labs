# Lab 04 — OpenCV and Real-Time Color Tracking

This laboratory introduces computer vision on the **Digilent Zybo legacy** running **PYNQ 3.0.1**. OpenCV processing runs on the ARM Processing System (PS). A **Logitech C270 USB webcam** is introduced early so that the exercises move quickly from static images to real-time vision.

## Hardware

- Digilent Zybo legacy
- PYNQ 3.0.1 image used by this repository
- Logitech C270 USB webcam
- Ethernet connection to the board
- No additional sensors are required

## Notebooks

| Notebook | Topic |
|---|---|
| [Lab04.1_OpenCV_Image_Basics.ipynb](Lab04.1_OpenCV_Image_Basics.ipynb) | Images, BGR/RGB, grayscale, pixels and regions of interest |
| [Lab04.2_USB_Webcam.ipynb](Lab04.2_USB_Webcam.ipynb) | Detecting and testing the Logitech C270 from Jupyter |
| [Lab04.3_HSV_and_Color_Masks.ipynb](Lab04.3_HSV_and_Color_Masks.ipynb) | HSV color space, thresholding and binary masks |
| [Lab04.4_Real_Time_Color_Detection.ipynb](Lab04.4_Real_Time_Color_Detection.ipynb) | Real-time red/green/blue/yellow detection |
| [Lab04.5_Contours_and_Object_Tracking.ipynb](Lab04.5_Contours_and_Object_Tracking.ipynb) | Contours, bounding boxes, area and object center |
| [Lab04.6_Color_Tracker_with_LEDs.ipynb](Lab04.6_Color_Tracker_with_LEDs.ipynb) | Integrated camera + color tracker + Zybo LED feedback |

## Learning outcomes

After completing the laboratory, students should be able to:

- load and inspect images with OpenCV;
- explain the BGR/RGB difference;
- convert images between BGR, RGB, grayscale and HSV;
- acquire frames from a USB webcam;
- construct HSV masks for selected colors;
- remove small mask artifacts using morphological operations;
- extract contours and object position;
- implement a simple real-time color tracker;
- connect a vision result to physical output on the Zybo board.

## Important Jupyter note

Do **not** use `cv2.imshow()` on the board. The notebooks display frames inline using IPython/Jupyter.

Always release the webcam after an experiment:

```python
cap.release()
```

If a camera cell is interrupted, run `cap.release()` manually before reopening the camera.

## Processing architecture

```text
Logitech C270
     |
     | USB
     v
Zynq ARM Processing System
     |
     | OpenCV / Python
     v
HSV -> mask -> contours -> object position
     |
     v
PYNQ GPIO -> Zybo LEDs
```

The laboratory deliberately performs the vision algorithms in software on the ARM processor. This establishes a baseline that can later be compared with FPGA-accelerated processing.
