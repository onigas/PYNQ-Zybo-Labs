"""CPU-only tests. Run: python -m pytest Lab07/tests -q"""
from pathlib import Path
import sys
import numpy as np
import cv2
import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'tools'))
from dma_threshold import reference_threshold


def test_complete_uint8_range():
    pixels = np.arange(256, dtype=np.uint8).reshape(16, 16)
    for threshold in (0, 1, 64, 127, 128, 129, 254, 255):
        output = reference_threshold(pixels, threshold)
        expected = np.where(pixels >= threshold, 255, 0).astype(np.uint8)
        np.testing.assert_array_equal(output, expected)
        assert np.all(np.isin(output, (0, 255)))


def test_sample_images_reference():
    root = Path(__file__).resolve().parents[1]
    image = cv2.imread(str(root/'images/scene_256.png'), cv2.IMREAD_GRAYSCALE)
    assert image is not None and image.shape == (256, 256)
    assert image.dtype == np.uint8
    for threshold in (0,64,128,192,255):
        result = reference_threshold(image,threshold)
        assert result.shape == image.shape
        assert np.array_equal(result, cv2.inRange(image, threshold, 255))


def test_bad_input():
    with pytest.raises(ValueError): reference_threshold(np.zeros((1,1), np.uint16), 128)
    with pytest.raises(ValueError): reference_threshold(np.zeros((1,1,3), np.uint8), 128)
    with pytest.raises(ValueError): reference_threshold(np.zeros((1,1), np.uint8), 256)
