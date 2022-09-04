import numpy as np
import glob
import matplotlib.pyplot as plt
import skimage.io
import skimage.color
import skimage.filters
from skimage.draw import polygon_perimeter
from skimage.measure import label, regionprops, perimeter
from skimage import filters, measure, morphology
import cv2 as cv

class KaloriMeter:
    def segment(self, height_image_path, area_image_path):
        # calculate height of object
        height_image = cv.imread(height_image_path, 0)
        blurred_height_image = cv.GaussianBlur(height_image, (5,5), 0)
        th = filters.threshold_otsu(blurred_height_image)
        binary_height_mask = blurred_height_image > th
        binary_height_mask = morphology.remove_small_objects(binary_height_mask, 50)
        binary_height_mask = morphology.remove_small_holes(binary_height_mask, 50)

        # create bounding box
        area_image_labels = label(binary_height_mask)
        bounding_box = []
        for region in regionprops(np.squeeze(area_image_labels), height_image):
            bbox = region.bbox
            print(region)
            bounding_box.append(bbox)
        print(bounding_box)

        with_boxes = np.copy(binary_height_mask)

        height = []
        for box in bounding_box:
            #[Xmin, Xmax, Ymin, Ymax]
            r = [box[2],box[0],box[0],box[2]]
            c = [box[3],box[3],box[1],box[1]]
            rr, cc = polygon_perimeter(r, c, binary_height_mask.shape)
            with_boxes[rr, cc] = 1 #set color white
            
            # calculate height
            rmax = box[2]
            rmin = box[0]
            height.append([(rmax-rmin) * 0.026458333])




        # calculate area of object
        area_image = cv.imread(area_image_path, 0)
        blurred_area_image = cv.GaussianBlur(area_image, (5,5), 0)
        ta = filters.threshold_otsu(blurred_area_image)
        binary_area_mask = blurred_area_image > ta
        binary_area_mask = morphology.remove_small_objects(binary_area_mask, 50)
        binary_area_mask = morphology.remove_small_holes(binary_area_mask, 50)

        height_image_labels = label(binary_area_mask)
            
        areas = []
        for region in regionprops(height_image_labels, area_image):
            area = region.area
            area = area * 0.026458333
            # print(area)

        # calculate perimeter of object
        # perimeter = perimeter(binary_mask, 4) * 0.026458333
        
        height = np.max(height)
        volume = area * height
        return area, height, volume

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
