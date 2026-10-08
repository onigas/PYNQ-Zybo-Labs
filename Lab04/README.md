# Lab 04 — OpenCV and USB Webcam Color Detection

Practical laboratory for **Digilent Zybo Legacy**, **PYNQ 3.0.1**, **OpenCV 4.5.4** and a **Logitech C270** USB webcam. The camera has been tested with V4L2 at `/dev/video0` (actual frame size: 640 × 480).

## Required setup

- Zybo Legacy with the tested PYNQ image and Jupyter.
- Logitech C270 connected to the USB port.
- Red, green and blue markers; stable lighting.
- Run each notebook top to bottom in a separate kernel. Do not run two notebooks accessing the camera concurrently.
- Do not install a different OpenCV version for this laboratory.

## Current notebooks

| Notebook | Topic | Status |
|---|---|---|
| [Lab04.1 — OpenCV Image Basics](Lab04.1_OpenCV_Image_Basics.ipynb) | Synthetic image, BGR/RGB, grayscale, grid and student-selected ROI | Revised |
| [Lab04.2 — USB Webcam](Lab04.2_USB_Webcam.ipynb) | Logitech C270 acquisition, warm-up, JPEG display and camera release | Revised |
| [Lab04.3 — HSV and RGB Color Detection](Lab04.3_HSV_and_Color_Masks.ipynb) | Red marker calibration, HSV + RGB filtering, simultaneous RED/GREEN/BLUE masks and contours | Revised |
| [Lab04.4 — Real-Time Color Detection](Lab04.4_Real_Time_Color_Detection.ipynb) | Earlier material, pending reorganization into tracking | Not yet revised |
| [Lab04.5 — Contours and Object Tracking](Lab04.5_Contours_and_Object_Tracking.ipynb) | Earlier tracking material, pending reorganization | Not yet revised |
| [Lab04.6 — Color Tracker with LEDs](Lab04.6_Color_Tracker_with_LEDs.ipynb) | Earlier LED experiment, pending reorganization | Not yet revised |

**Important:** Lab04.3 now combines the previously separate red-marker and three-color experiments. Lab04.4–Lab04.6 are retained unchanged until the next redesign/test cycle; they do not yet match the proposed five-notebook end structure. No parallel versions have been added.

## Recommended sequence

1. In Lab04.1, generate `images/colored_shapes.png` and use the grid to estimate coordinates for an ROI without being given its bounds.
2. In Lab04.2, capture an image from the C270 and confirm that the camera can be opened again on subsequent runs.
3. In Lab04.3, run the red-marker detector, then the three-color detector and compare their binary masks.

## Camera handling

The acquisition helper opens `/dev/video0` through `cv2.CAP_V4L2`, requests 640 × 480, discards 30 warm-up frames, then releases the device with `try/finally`. Display is inline in Jupyter; **do not use** `cv2.imshow()`. If opening fails, check other notebooks/kernels before changing device settings. The time delay between warm-up frames assists exposure stabilization.

## Interpreting the results

- RED detection uses two HSV hue bands because red wraps around the hue boundary.
- The red-marker exercise adds a height/width filter for a **vertical marker only**.
- The RGB exercise detects **colored regions**, not entire physical objects. White writing/labels can split one marker into multiple contours.
- During experiments with three markers, RED: 2, GREEN: 2, BLUE: 1 regions were observed. Parameters may need adjustment under other illumination.

## Verification

The camera, color detection thresholds and outputs were tested experimentally in the earlier iterative work. These newly consolidated notebook files still require a complete top-to-bottom execution on Zybo.
