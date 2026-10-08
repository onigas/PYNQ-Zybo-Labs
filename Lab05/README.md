# Lab05 – Traffic Sign Recognition (OpenCV)

Target: **Zybo legacy / PYNQ 3.0.1**, Jupyter Notebook, Python, NumPy, OpenCV, Matplotlib. No FPGA overlay or webcam required.

## Contents

| Notebook | Topic |
|---|---|
| `Lab05.1_Traffic_Sign_Color_Segmentation.ipynb` | HSV thresholding; red and blue masks |
| `Lab05.2_Traffic_Sign_Shape_Detection.ipynb` | Contours; polygon approximation; bounding boxes |
| `Lab05.3_Traffic_Sign_Recognition.ipynb` | Rule-based sign recognition; performance limits |

`images/traffic_signs.png` contains all six classes; `images/test_01.png`–`test_03.png` supply additional examples. All images are original, reproducibly generated synthetic teaching assets.

## Installation and operation

1. Download and extract the **entire** `Lab05` folder.
2. Upload the notebooks **and the `images` folder** to the same `Lab05` directory in Jupyter on Zybo.
3. Open each notebook in numerical order and run cells from top to bottom.
4. All paths are relative to the notebook directory (`images/...`).

Do not overwrite the PYNQ system OpenCV installation. The notebook displays the installed OpenCV version. The APIs used are compatible with OpenCV 3 and 4.

## Expected behaviour

- Lab05.1 separates red and blue sign pixels.
- Lab05.2 locates candidate regions and reports shapes.
- Lab05.3 classifies synthetic STOP, NO ENTRY, WARNING, PARKING and MANDATORY DIRECTION examples. Speed limit **number recognition is not implemented**; it is intentionally labelled `SPEED LIMIT (candidate)`.

## Scope

The test images are idealized and axis-aligned. Performance on real signs under variable lighting, perspective, background clutter, and occlusion is not guaranteed. This is a classical OpenCV foundation for later FPGA acceleration, not a vehicle perception system.

## Reading the notebooks

Every code cell is preceded by a short description of its purpose. Lab05.2 and Lab05.3 also display intermediate masks, candidate contours and detected shapes, so students can follow the pipeline before the final output. Some function-definition cells do not themselves produce figures; execute the next visual checkpoint to inspect their results.
