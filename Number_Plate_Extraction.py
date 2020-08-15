import cv2
import glob
import numpy as np

def detect_licence_plate(image):
	""" Shows a green bounding box near licence plate, if detected
	Args:
		filename : An image to detect the license plate

	Returns:
		None

	"""
	#Downsample the input image and convert it to grayscale image.
	rgb = cv2.pyrDown(image)
	downsampled_image = cv2.cvtColor(rgb, cv2.COLOR_BGR2GRAY)

	#Morph gradient allows us to get outlines in the image.
	kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
	grad = cv2.morphologyEx(downsampled_image, cv2.MORPH_GRADIENT, kernel)

	#Otsu's thresholding with binary thresh works well in removing noise.
	_, bw = cv2.threshold(grad, 0.0, 255.0, cv2.THRESH_BINARY | cv2.THRESH_OTSU)

	#Thickens lines(dilation) after processing a rectangular kernel.
	kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (9, 1))
	connected = cv2.morphologyEx(bw, cv2.MORPH_CLOSE, kernel)

	#Contours are detected for all connected points(white text on black background only)
	contours, hierarchy = cv2.findContours(connected.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
	mask = np.zeros(bw.shape, dtype=np.uint8)

	for idx in range(len(contours)):
		x, y, w, h = cv2.boundingRect(contours[idx])
		mask[y:y+h, x:x+w] = 0
		cv2.drawContours(mask, contours, idx, (255, 255, 255), -1)

		#Obtain a color count 
		r = float(cv2.countNonZero(mask[y:y+h, x:x+w])) / (w * h)

		#Only draw those contours whose width is atlease twice the height(for license plate) and are rectangular.
		if r > 0.45 and w > 2*h and h > 4:
			cv2.rectangle(rgb, (x, y), (x+w-1, y+h-1), (0, 255, 0), 2)

	cv2.imshow('Output Image', rgb)
	cv2.waitKey(0)


filenames = glob.glob("car_images\\*.jpg")
array_of_images = [cv2.imread(img) for img in filenames]

for img in array_of_images:
	detect_licence_plate(img)