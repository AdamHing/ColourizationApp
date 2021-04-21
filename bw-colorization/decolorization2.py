# python decolorization2.py --image images/red-and-white-raccoon.jpg
import cv2
import argparse

ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", type=str,
	help="Path to image")
args = vars(ap.parse_args())

colourimage = cv2.imread(args["image"])
grayimage = cv2.cvtColor(colourimage, cv2.COLOR_BGR2GRAY)
cv2.imshow("grayimage",grayimage)
cv2.waitKey(0)