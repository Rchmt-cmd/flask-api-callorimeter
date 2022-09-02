import numpy as np
import glob
import matplotlib.pyplot as plt
import skimage.io
import skimage.color
import skimage.filters
from skimage import data, filters, measure, morphology
import cv2 as cv

class KaloriMeter:
    def segment(self, image_path):
        image = cv.imread(image_path, 0)

        blurred_image = cv.GaussianBlur(image, (5,5), 0)
        t = filters.threshold_otsu(blurred_image)
        binary_mask = blurred_image > t
        binary_mask = morphology.remove_small_objects(binary_mask, 50)
        binary_mask = morphology.remove_small_holes(binary_mask, 50)
        labels = measure.label(binary_mask)
        for region in measure.regionprops(labels, image):
            area = region.area
            area = area / 78
            print(area)


        return labels.reshape((image.shape[0],image.shape[1])),binary_mask.astype(np.uint8)

    def calories(self, binary_mask):
        w = binary_mask.shape[1]
        h = binary_mask.shape[0]
        area=round((w*h)/78)
        return area


if __name__=="main":
    kaloriMeter = KaloriMeter()
    segment = kaloriMeter.segment('nasi.jpg')
    calories = kaloriMeter.calories(segment)
    cv.imshow('segment', segment)
    cv.waitKey(0)
