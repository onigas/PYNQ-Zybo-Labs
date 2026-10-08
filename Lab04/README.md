# Lab 04 — OpenCV and Color Tracking

A practical laboratory for **Zybo legacy / PYNQ 3.0.1**, using **OpenCV 4.5.4** and the **Logitech C270**. Vision processing runs on the ARM Processing System. The last experiment connects the result to the board LEDs.

## Before starting

- Use the board and camera setup already verified in this course: Linux V4L2, `/dev/video0`, 20 discarded warm-up frames, inline JPEG display in Jupyter, and `cap.release()`.
- Open the notebooks on the Zybo in the Python 3 environment where OpenCV 4.5.4 already works. Do not reinstall or upgrade OpenCV for this lab.
- Have green and blue objects (colored paper or plastic), a simple background and steady room lighting.
- Run each notebook top to bottom, with the working directory set to `Lab04`. Lab04.1 generates `images/colored_shapes.png`, which Lab04.3 uses.
- Use only one camera notebook at a time. Variables and device settings are not shared between notebook kernels.
- The first exercise is a short introduction (about 10 minutes); the camera is introduced immediately afterward.

## Guided experiments

| Notebook | Activity |
|---|---|
| [Lab04.1](Lab04.1_OpenCV_Image_Basics.ipynb) | Generate an image, inspect pixels and select a region |
| [Lab04.2](Lab04.2_USB_Webcam.ipynb) | Capture a real frame and run a short live preview |
| [Lab04.3](Lab04.3_HSV_and_Color_Masks.ipynb) | Compare the image, raw mask and cleaned mask |
| [Lab04.4](Lab04.4_Real_Time_Color_Detection.ipynb) | Show two colored objects and adjust the area threshold |
| [Lab04.5](Lab04.5_Contours_and_Object_Tracking.ipynb) | Observe bounding box, centroid, area and LOST |
| [Lab04.6](Lab04.6_Color_Tracker_with_LEDs.ipynb) | Move one object to light LD0, LD1 or LD2; remove it for LD3 |

All working code is supplied. Exercises ask students to observe results or change one parameter at a time. There is no large final programming assignment, switch/button controller, or required multi-object tracking extension.

## Experimentally validated color detection tasks

These additional, self-contained notebooks document the Logitech C270 tests performed on the Zybo. They supplement the numbered Lab04 notebooks without replacing the existing introduction or webcam acquisition exercises.

| Task | Notebook | Verified behavior |
|---|---|---|
| Task 4.1 — Red marker detection | [Task4.1_Red_Marker_Detection.ipynb](Task4.1_Red_Marker_Detection.ipynb) | One vertical red-marker region, with hand detections suppressed |
| Task 4.2 — RGB color-region detection | [Task4.2_RGB_Color_Detection.ipynb](Task4.2_RGB_Color_Detection.ipynb) | Three markers identified; RED: 2 regions, GREEN: 2 regions, BLUE: 1 region |

Both notebooks use `/dev/video0`, V4L2, a 640×480 capture request, 30 warm-up frames, inline JPEG display and camera release via `finally`. Comments and student instructions are in English.

The RGB task counts segmented color regions, **not complete objects**. White printed areas can split one marker into multiple contours. Thresholds are empirical and may need adjustment under different lighting.

## Camera operation

Each camera notebook includes the same supplied helper. It opens `CAMERA_DEVICE`, checks that the camera opened, requests 640×480, discards 20 frames and validates every read. Check `frame.shape` for the actual negotiated resolution.

The `with camera_session()` block uses `try/finally` to release the camera on normal completion, Python errors and ordinary kernel interrupts. Still-image processing takes place after camera release. Live sessions have both a frame limit and a time limit, measured after warm-up. A blocked USB driver read can delay a timeout or interrupt; this is not a driver watchdog.

If capture fails:

1. Shut down other kernels that may hold the camera; closing a browser tab is not enough.
2. For older code without cleanup, run `cap.release()` in the kernel that opened it.
3. Inspect `/dev/video*` and `fuser -v /dev/video0` using the optional check in Lab04.2.
4. If a read remains blocked, restart/shut down the owning kernel; reconnect the camera if necessary.
5. If the capture device path changed, set `CAMERA_DEVICE` in each notebook you use. Do not blindly assume a second video node provides images.

Images are displayed inside Jupyter; no `cv2.imshow()` window is required.

## LED experiment

Lab04.6 uses the same interface as Lab01 and Lab03:

`Overlay("base.bit") → ol.leds_gpio.channel1 → setdirection("out") → setlength(4)`

The LEDs show LEFT, CENTER, RIGHT and LOST relative to the displayed image. They are switched off when the session exits. No new overlay is needed.

## What students record

- Actual camera resolution.
- One observation about changing a mask threshold or lighting.
- One centroid coordinate and its horizontal region.
- Whether all four LED states worked.

## References and verification

- [OpenCV 4.5.4: color spaces and masks](https://docs.opencv.org/4.5.4/df/d9d/tutorial_py_colorspaces.html)
- [OpenCV 4.5.4: contour features](https://docs.opencv.org/4.5.4/dd/d49/tutorial_py_contour_features.html)
- [PYNQ AXI GPIO interface](https://pynq.readthedocs.io/en/v3.0.0/pynq_package/pynq.lib/pynq.lib.axigpio.html)

Camera acquisition was previously verified on the board. These revised notebooks reuse that acquisition sequence and the GPIO interface from earlier labs; the complete revised notebooks still require an end-to-end run on Zybo. No new hardware execution is claimed.
