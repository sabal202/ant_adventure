#-*- coding cp1251 -*-#
import numpy as np
import cv2
import diagram as dg
import matplotlib.pyplot as plt

# read coordinatesof field (use set_coordinates_for_field)
coordinatesFile = open("coordinates_of_field.txt")
coordinatesFromFile = coordinatesFile.readline().split(" ")
coordinatesFromFile = [int(i) for i in coordinatesFromFile]
l, u, r, d = coordinatesFromFile
coordinatesFile.close()
# l, u, r, d = 432, 18, 1464, 1028 # left, up, right, down 432 18 1464 1028

track = []  # list for path
trackFile = open("track.txt", "w")
averageVelocityListFile = open("averageVelocity.txt", "w")
valuesOfMovingInCenter = open('valuesOfMovingInCenter.txt', "w")

fps = 25  # frames per second in video
deltaTime = 10  # time which used in count of delta values
fieldWidth = 10  # (cm) real width of area
path = 0  # counter of path of ant`s moving in cm
scale = 1.3  # scale for decreasing frames
framesCount = 0  # counter for frames
videoFile = "00028.mts"  # name of video file
seconds = 0  # counter for real time in seconds

quitKey = 27  # (esc) key to close window
deltaPath = 0
deltaPathInFrame = 0  # length of path in delta time
deltaVelocity = 0

width = r - l
height = d - u

secondsForStayTime = 0
countFramesForMoveTime = 0
framesForMoveInCenter = 0
framesCount = 0

lastCoordinates = None

countFramesForStayTime = 0

VIDEO_RECORD = False

# resize window to working area


def toFieldCoordinates(frame):
    frame = frame[u: d, l: r]
    width, height, z = frame.shape
    frame = cv2.resize(frame, (int(height / scale), int(width / scale)))
    return frame

# delete bacground with image of background
# you can get background image with background_create.py


def delete_background(frame):
    thresholdForGrayscale = 10

    # open background image
    background = cv2.imread('summ.png', 0)

    # convert colors to gray
    grayscaleFrame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # retype frame from uint8 to int16
    grayscaleFrame = grayscaleFrame.astype(np.int16)

    # delete background
    grayscaleFrame = grayscaleFrame - background

    # delete negative values
    grayscaleFrame[np.abs(grayscaleFrame) < 40] = 0

    # retype frame from int16 to uint8
    grayscaleFrame = grayscaleFrame.astype(np.uint8)

    # thresholding image
    ret, binaryFrame = cv2.threshold(grayscaleFrame, thresholdForGrayscale,
                                     255, cv2.THRESH_BINARY)
    return binaryFrame


# record video of work?
if VIDEO_RECORD:
    fourcc = cv2.VideoWriter_fourcc(*'DIVX')
    out = cv2.VideoWriter('output.avi', fourcc, 25, (int((r - l) / scale),
                                                     int((d - u) / scale)))
    black_white_out = cv2.VideoWriter('black_white.avi', fourcc, 25,
                                      (int((r - l) / scale), int((d - u) / scale)))

# capture the video
cap = cv2.VideoCapture(videoFile)

while True:
    # get next frame
    ret, frame = cap.read()

    #np.zeros((int(width / scale), int(height / scale)))

    # close window checker
    pauseSwitch = False
    pressedKey = cv2.waitKey(1)
    if pressedKey & 0xFF == quitKey or not ret:
        break
    # pause video key
    elif pressedKey & 0xFF == ord(' '):
        pressedKey = cv2.waitKey(0)
        while pressedKey != ord(' '):
            if pressedKey == quitKey:
                pauseSwitch = True
                break
            pressedKey = cv2.waitKey(0)

    if pauseSwitch:
        break

    # resize area
    frame = toFieldCoordinates(frame)

    grayscaleFrame = delete_background(frame)
    additionalFrame = grayscaleFrame.copy()
    widthA, heightA = additionalFrame.shape
    additionalFrame = cv2.resize(
        additionalFrame, (int(heightA / scale), int(widthA / scale)))
    if VIDEO_RECORD:
        black_white_out.write(cv2.cvtColor(grayscaleFrame, cv2.COLOR_GRAY2BGR))

    # find contours
    contours = cv2.findContours(grayscaleFrame, cv2.RETR_EXTERNAL,
                                cv2.CHAIN_APPROX_SIMPLE)[-2]

    if len(contours):
        # find coordinates of ant
        listOfAreas = [cv2.contourArea(i) for i in contours]
        maxContour = contours[listOfAreas.index(max(listOfAreas))]
        (x, y), radius = cv2.minEnclosingCircle(maxContour)
        coordinates = (int(x), int(y))

        # draw contours
        cv2.drawContours(frame, maxContour, -1, (255, 255, 0), 1)

        # add path and track
        if len(track):
            deltaPathInFrame = ((x - track[-1][0]) ** 2 +
                                (y - track[-1][1]) ** 2) ** 0.5
            path += deltaPathInFrame
            deltaPath += deltaPathInFrame
        track.append(coordinates)

        # write coordinates in file
        trackFile.write(" ".join([str(i) for i in coordinates]) + "\n")

    x = int(x)
    y = int(y)

# stay/move time
    if len(track) > 1:

        # getting number of frame for move/stay time and counting seconds
        if deltaPathInFrame < 5:
            countFramesForStayTime += 1

            if (countFramesForStayTime % fps == 0):
                secondsForStayTime += 1
        else:
                # print('meow')
            countFramesForMoveTime += 1 + countFramesForStayTime % fps
            countFramesForStayTime = 0

        # time of move
        secondsForMoveTime = countFramesForMoveTime / fps

    # render stay time
        cv2.putText(additionalFrame, 'stay time: ' + str(secondsForStayTime)
                    + ' seconds', (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0))

    # render move time
        cv2.putText(additionalFrame, 'move time: ' + str(secondsForMoveTime)
                    + ' seconds', (10, 70), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0))

    # time when ant moved in center
    # checking coordinate x and y in 1/2 of window in center
    if x < ((((width / scale) / 4) * 3)) and x > ((width / scale) / 4) \
            and y < (((height / scale) / 4) * 3) and y > ((height / scale) / 4):
        framesForMoveInCenter += 1

    # devide number of framesCount by 25 (fps) and getting time in seconds
    secondsForMoveInCenter = framesForMoveInCenter / fps

    if framesCount % 250 == 0:
        valuesOfMovingInCenter.write(str(secondsForMoveInCenter) + '\n')

    framesCount += 1

    # render time of move in center

    cv2.putText(additionalFrame, 'move in center: ' + str(secondsForMoveInCenter)
                + ' seconds', (10, 110), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0))

    # draw ant`s track
    for i in range(0, len(track) - 1):
        if i < len(track) - 100:
            frame = cv2.line(frame, track[i], track[i + 1], (100, 100, 100), 5)
        else:
            frame = cv2.line(frame, track[i], track[i + 1], (0, 255, 0), 5)

    # increase frame number
    framesCount += 1

    if framesCount % fps == 0:
        seconds += 1

    # get delta parametrs in delta time and write them on window
    if framesCount % deltaTime == 0:
        deltaVelocity = round(deltaPath * fps / width
                              * fieldWidth / deltaTime, 2)
        deltaPath = 0

        averageVelocityListFile.write(str(deltaVelocity) + "\n")

    cv2.putText(additionalFrame, "velocity: " + str(deltaVelocity), (10, 50),
                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 1)
    cv2.putText(additionalFrame, "real time: " + str(seconds) + " seconds", (10, 90),
                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 1)

    if VIDEO_RECORD:
        out.write(frame)

    # show frame in 2 windows
    cv2.imshow("Frame", frame)
    cv2.imshow("information", additionalFrame)

averageVelocityListFile.close()
trackFile.close()
path = path * fieldWidth / width
cap.release()

if VIDEO_RECORD:
    out.release()
    black_white_out.release()

cv2.putText(additionalFrame, str(framesCount) + " framesCount",
            (10, 200), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0))

# write length of path
cv2.putText(additionalFrame, str(round(path, 2)) + "cm(len of path)",
            (10, 300), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0))

# write average velocity
cv2.putText(additionalFrame, str(round(path / framesCount * fps, 2))
            + "cm per sec(average velocity)",
            (10, 250), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0))

# show frame
cv2.imshow("information", additionalFrame)
cv2.waitKey(0)
# quit when you press any button
cv2.destroyAllWindows()
valuesOfMovingInCenter.close()

# write stats
file = open("output.txt", "w")
file.write(str(round(path, 2)) + "cm(len of path)\n"
           + str(round(path / framesCount * fps, 2))
           + "cm per sec(average velocity)\n"
           + str(round(secondsForMoveInCenter * 100 / framesCount, 2))
           + "%(time in coordinates/ all time)")

file.close()

dg.velodiagram("averageVelocity.txt", file=True)
dg.threeD_Graf("track.txt", file=True)
dg.piechart(secondsForStayTime, secondsForMoveTime)
dg.antsInCenterDiagram("valuesOfMovingInCenter.txt", file=True)
velodiagramImg = cv2.imread('velodiagram.png', 1)
antsInCenterDiagram = cv2.imread('center.png', 1)
threeD_GrafImg = cv2.imread('3dGraph.png', 1)
piechartImg = cv2.imread('piechart.png', 1)

images = [velodiagramImg, antsInCenterDiagram, threeD_GrafImg, piechartImg]

for i in range(4):
    plt.subplot(2, 2, i + 1), plt.imshow(images[i], 'gray')
    plt.xticks([]), plt.yticks([])

plt.show()
