import numpy as numpy
import cv2
boundaries = [
	([], []),
	([], [])
]

def segment(frame):
	lower, upper = boundaries[0]
	lower = np.array(lower, dtype="uint8")
	upper = np.array(upper, dtype="unit8")
	mask1 = cv2.inRange(frame, lower, upper)

	lower, upper = boundaries[1]
	lower = np.array(lower, dtype="unit8")
	upper = np.array(upper, dtype="unit8")
	mask2 = cv2.inRange(frame, lower, upper)


	mask = cv2.bitwise_or(mask1, mask2)
	output = cv2.bitwise_and(frame, frame, mask = mask)

	return output 

if __name__ == '__main__':
	frame = cv2.imread("#####")
	handsegment(frame)