from pyimagesearch.shapedetector import ShapeDetector
from pyimagesearch.colorlabeler import ColorLabeler
import imutils
import cv2
from sklearn.cluster import KMeans
import utils
import numpy as np

actualimage = 'testfiles/shapes7.jpg'
image = cv2.imread(actualimage)
image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
image = image.reshape((image.shape[0] * image.shape[1], 3))

clt = KMeans(n_clusters = 3)
clt.fit(image)

hist = utils.centroid_histogram(clt)
index = np.argmax(hist)

bar = utils.plot_colors(hist, clt.cluster_centers_)

a=0
b=0

for i in range(3):
    j = clt.cluster_centers_[index][i]
    if j > 0 and j< 50:
        a=a+1
    elif j > 225 and j < 256:
        b=b+1
    else:
        print("Something go wrong")

if a >= 3:
	print("background is black")
	image = cv2.imread(actualimage)

	blurred = cv2.GaussianBlur(image, (5, 5), 0)
	gray = cv2.cvtColor(blurred, cv2.COLOR_BGR2GRAY)
	lab = cv2.cvtColor(blurred, cv2.COLOR_BGR2LAB)

	thresh = cv2.threshold(gray, 60, 255, cv2.THRESH_BINARY)[1]

	cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
	cnts = imutils.grab_contours(cnts)

	sd = ShapeDetector()
	cl = ColorLabeler()
	f = 0
	for c in cnts:
		M = cv2.moments(c)
		cX = int(M["m10"] / (M["m00"] + 1e-7))
		cY = int(M["m01"] / (M["m00"] + 1e-7))

		# detect the shape of the contour and label the color
		shape,scounter = sd.detect(c)
		color = cl.label(lab, c)
		if color != "black":
			text = "{} {}".format(color, shape)
			cv2.drawContours(image, [c], 0, (0, 0, 255), 2)
			cv2.putText(image, text, (cX, cY), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255,0,0), 0)
			f=f+1
	print(f,"Shapes")
	print(scounter)
	cv2.imshow("Image", image)
	cv2.waitKey(0)
elif b>=3:
	print("background is white")
	image = cv2.imread(actualimage)

	blurred = cv2.GaussianBlur(image, (5, 5), 0)
	gray = cv2.cvtColor(blurred, cv2.COLOR_BGR2GRAY)
	lab = cv2.cvtColor(blurred, cv2.COLOR_BGR2LAB)

	thresh = cv2.threshold(gray, 240, 255, cv2.THRESH_BINARY)[1]

	cnts = cv2.findContours(thresh.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
	cnts = imutils.grab_contours(cnts)

	sd = ShapeDetector()
	cl = ColorLabeler()
	f=0
	for c in cnts:
		M = cv2.moments(c)
		cX = int(M["m10"] / (M["m00"] + 1e-7))
		cY = int(M["m01"] / (M["m00"] + 1e-7))
		# detect the shape of the contour and label the color
		shape = sd.detect(c)
		color = cl.label(lab, c)
		if color != "white":
			text = "{} {}".format(color, shape)
			cv2.drawContours(image, [c], 0, (0, 255, 0), 2)
			cv2.putText(image, text, (cX, cY), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 0)
			f=f+1

	print(f-1,"Shapes")
	cv2.imshow("Image", image)
	cv2.waitKey(0)
