import numpy as np 
import cv2

cap = cv2.VideoCapture("00028.MTS")

# read coordinatesof field (use set_coordinates_for_field)
coordinatesFile = open("coordinates_of_field.txt")
coordinatesFromFile = coordinatesFile.readline().split(" ")
coordinatesFromFile = [int(i) for i in coordinatesFromFile]
l, u, r, d = coordinatesFromFile
coordinatesFile.close()

scale = 1.3
frameNum = 1
frameMax = 6000 

def toField(frame):
	frame = frame[u : d, l : r]
	w, h, z = frame.shape
	frame = cv2.resize(frame, (int(h / scale), int(w / scale)))
	return frame

cv2.namedWindow('window')
ret, frame = cap.read()
frame = toField(frame)
frame = np.divide(frame, frameMax)
framesumm = frame

while frameNum <= frameMax and cap.isOpened():

	if cv2.waitKey(1) & 0xFF == ord('q'):
		break

	ret, frame = cap.read()
	frame = toField(frame)

	frame = np.divide(frame, frameMax)
	framesumm = np.add(framesumm, frame)

	frameNum += 1
	

cv2.imwrite('summ.png', framesumm)

cap.release()
cv2.destroyAllWindows()