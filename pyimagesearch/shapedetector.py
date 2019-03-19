# import the necessary packages
import cv2

class ShapeDetector:
	def __init__(self):
		pass

	ctri = 0
	crec = 0
	csqr = 0
	ccrc = 0
	cpnt = 0
	def detect(self,c):
		# initialize the shape name and approximate the contour
		shape = "unidentified"
		peri = cv2.arcLength(c, True)
		approx = cv2.approxPolyDP(c, 0.01 * peri, True)

		list = []
		# if the shape is a triangle, it will have 3 vertices
		if len(approx) == 3:
			shape = "triangle"
			self.ctri=self.ctri+1

		# if the shape has 4 vertices, it is either a square or
		# a rectangle
		elif len(approx) == 4:
			# compute the bounding box of the contour and use the
			# bounding box to compute the aspect ratio
			(x, y, w, h) = cv2.boundingRect(approx)
			ar = w / float(h)

			# a square will have an aspect ratio that is approximately
			# equal to one, otherwise, the shape is a rectangle
			if ar >= 0.95 and ar <= 1.05:
				 shape="square"
				 self.csqr=self.csqr+1
			else:
				shape= "rectangle"
				self.crec=self.crec+1

		# if the shape is a pentagon, it will have 5 vertices
		elif len(approx) == 5:
			shape = "pentagon"
			self.cpnt=self.cpnt+1
			print(self.cpnt)

		# otherwise, we assume the shape is a circle
		else:
			shape = "circle"
			self.ccrc=self.ccrc+1

		list.append(self.crec)
		list.append(self.csqr)
		list.append(self.ctri)
		list.append(self.cpnt)
		list.append(self.ccrc)
		# return the name of the shape
		return shape,list