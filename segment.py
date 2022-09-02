import cv2
import numpy as np
import glob
import matplotlib.pyplot as plt
import skimage.io
import skimage.color
import skimage.filters
from skimage.measure import label, regionprops, regionprops_table

class Segment:
    def __init__(self,segments=2):
        #define number of segments, with default 5
        self.segments=segments

    def kmeans(self,image):
        image=cv2.GaussianBlur(image,(7,7),0)
        vectorized=image.reshape(-1,3)
        vectorized=np.float32(vectorized) 
        criteria=(cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 10, 1.0)
        ret,label,center=cv2.kmeans(vectorized,self.segments,None,criteria,10,cv2.KMEANS_RANDOM_CENTERS)
        res = center[label.flatten()]
        segmented_image = res.reshape((image.shape))
        props = regionprops(label)
        for region in props:
            area = region.area
            area = area / 78
            print(area)
        return label.reshape((image.shape[0],image.shape[1])),segmented_image.astype(np.uint8)

    def measure_area(filename, sigma=1.0):

        # read the original image, converting to grayscale on the fly
        image = skimage.io.imread(fname=filename, as_gray=True)

        # blur before thresholding
        blurred_image = skimage.filters.gaussian(image, sigma=sigma)

        # perform automatic thresholding to produce a binary image
        t = skimage.filters.threshold_otsu(blurred_image)
        binary_mask = blurred_image > t

        # determine root mass ratio
        rootPixels = np.count_nonzero(binary_mask)
        w = binary_mask.shape[1]
        h = binary_mask.shape[0]
        density = rootPixels / (w * h)
        area=round((w*h)/78)

        return area


    def extractComponent(self,image,label_image,label):
        component=np.zeros(image.shape,np.uint8)
        component[label_image==label]=image[label_image==label]
        return component

if __name__=="__main__":
    import argparse
    import sys
    ap = argparse.ArgumentParser()
    ap.add_argument("-i", "--image", required = True, help = "Path to the image")
    ap.add_argument("-n", "--segments", required = False, type = int,
        help = "# of clusters")
    args = vars(ap.parse_args())

    image=cv2.imread(args["image"])
    if len(sys.argv)==3:
        
        seg = Segment()
        label,result= seg.kmeans(image)
    else:
        seg=Segment(args["segments"])
        label,result=seg.kmeans(image)
    cv2.imshow("segmented",result)
    result=seg.extractComponent(image,label,2)
    cv2.imshow("extracted",result)
    cv2.waitKey(0)