import cv2
import numpy as np

# capture the video
cap = cv2.VideoCapture("00028.mts")

coordinates_file = open("coordinates_of_field.txt", "w")  
scale = 2
lu_x, lu_y = -1, -1 # coordinates left up point
rd_x, rd_y = -1, -1 # coordinates right down point
switch_for_points = True # True/False = first/second point


ret, frame_origin = cap.read()
cv2.namedWindow('Select field coordinates') 
width, height, z = frame_origin.shape
frame_origin = cv2.resize(frame_origin, (int(height / scale), int(width / scale)))

cv2.imshow('Select field coordinates', frame_origin) 
frame = frame_origin.copy()


# mouse callback function 
def set_coordinates(event, x, y, flags, param): 
	global lu_x, lu_y, rd_x, rd_y, switch_for_points, frame
	if event == cv2.EVENT_LBUTTONUP: 
		if switch_for_points:
			lu_x, lu_y = x, y
			cv2.line(frame, (x, y), (x, y), (255, 0, 0), 5)
		else:
			rd_x, rd_y = x, y
			cv2.line(frame, (x, y), (x, y), (0, 255, 0), 5)
		switch_for_points = not switch_for_points

cv2.setMouseCallback('Select field coordinates', set_coordinates)
flag = 1

while(1): 
	cv2.putText(frame, "Select two points of area, first - up left, second - down right ", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1)
	cv2.putText(frame, '"d" - to draw rectangle ', (50, 70), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1)
	cv2.putText(frame, '"q" - to clear ', (50, 90), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1)
	cv2.putText(frame, '"Esc" - to close window', (50, 110), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1)
	cv2.imshow('Select field coordinates', frame) 
	k = cv2.waitKey(1) & 0xFF  
	if k == ord('d') and flag:
		cv2.rectangle(frame, (lu_x, lu_y), (rd_x, rd_y), (255, 30, 30), 1) 
	elif k == 27:
		break
	elif k == ord('q') or k == 233 or k == ord('c'):
		cv2.imshow('Select field coordinates', frame_origin) 
		frame = frame_origin.copy()
		lu_x, lu_y = -1, -1
		rd_x, rd_y = -1, -1

coordinates_list = [lu_x, lu_y , rd_x, rd_y]
coordinates_file.write(" ".join([str(i * scale) for i in coordinates_list]) + "\n")
coordinates_file.close()
cv2.destroyAllWindows()

