"""Human-readable labels for official GTSRB class IDs 0..42.

Lab08.1 only needs these names; the pretrained BNN uses its own classes.txt,
which adds an additional class 43 (Not a roadsign).
"""
LABELS = ['20 Km/h','30 Km/h','50 Km/h','60 Km/h','70 Km/h','80 Km/h','End 80 Km/h','100 Km/h','120 Km/h','No overtaking','No overtaking for large trucks','Priority crossroad','Priority road','Give way','Stop','No vehicles','Vehicles over 3.5t prohibited','No entry','Danger ahead','Bend left','Bend right','Double bend','Uneven road','Slippery road','Road narrows right','Road works','Traffic signals','Pedestrians','Children crossing','Bicycles prohibited','Snow or ice','Wild animals','End of speed/overtaking restrictions','Turn right ahead','Turn left ahead','Ahead only','Ahead or right','Ahead or left','Keep right','Keep left','Roundabout','End of no overtaking','End of no overtaking for trucks']

def load_rgb_32(image_path):
    """Load one GTSRB photograph as 32x32 RGB uint8 for the compact FPGA.

    Unlike the separate ARM BNN preprocessing, this version resizes directly
    (OpenCV INTER_LINEAR) and returns interleaved RGB for AXI DMA.
    """
    import cv2
    image_bgr = cv2.imread(str(image_path), cv2.IMREAD_COLOR)
    if image_bgr is None:
        raise IOError("Cannot read GTSRB image: {}".format(image_path))
    small_bgr = cv2.resize(image_bgr, (32, 32), interpolation=cv2.INTER_LINEAR)
    return cv2.cvtColor(small_bgr, cv2.COLOR_BGR2RGB)
