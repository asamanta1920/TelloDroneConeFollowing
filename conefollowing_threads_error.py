from djitellopy import Tello
import cv2
import numpy as np
import time

# VARIABLES

######################################################################
width = 320 # WIDTH OF THE IMAGE
height = 240 # HEIGHT OF THE IMAGE
startCounter = 0 # 0 FOR FLIGHT 1 FOR TESTING
# HSV VALUES
HSV_LOWER = np.array([0, 150, 141])
HSV_UPPER = np.array([10, 255, 255])
EXIST_SIZE = 5 # MIN SIZE
######################################################################

# FUNCTIONS

######################################################################
def find_contours(image):

    image_hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    mask = cv2.inRange(image_hsv, HSV_LOWER, HSV_UPPER)

    contours = cv2.findContours(mask, 3, 2)[0]

    return contours, mask

def check_contours_exist(contours):

    greatest_contour = None

    if not(contours):

        return (False, greatest_contour)

    greatest_contour = max(contours, key = cv2.contourArea)

    area = cv2.contourArea(greatest_contour)

    if area < EXIST_SIZE:

        return (False, greatest_contour)

    return (True, greatest_contour)
######################################################################

# CONNECT TO TELLO
me = Tello()
me.connect()
# me.for_back_velocity = 0
# me.left_right_velocity = 0
# me.up_down_velocity = 0
# me.yaw_velocity = 0
# me.speed = 0

print(me.get_battery())

me.streamoff()
me.streamon()
time.sleep(1)

# GET THE IMAFE FROM TELLO
frame_read = me.get_frame_read()
myFrame = frame_read.frame
img = cv2.resize(myFrame, (width, height))

# DISPLAY IMAGE
cv2.imshow("Drone Video Feed", img)

time.sleep(30)

while True:

    # GET THE IMGAE FROM TELLO
    frame_read = me.get_frame_read()
    myFrame = frame_read.frame
    img = cv2.resize(myFrame, (width, height))

    # GET CONTOURS
    contours, mask = find_contours(img)

    # GET GREATEST CONTOUR
    contours_exist, greatest_contour = check_contours_exist(contours)

    # DRAW GREATEST CONTOURS
    cv2.drawContours(img, contours, -1, (0, 255, 0), 3)

    # DISPLAY IMAGE
    cv2.imshow("Drone Video Feed", img)

    # TO GO UP IN THE BEGINNING
    if startCounter == 10:
        me.takeoff()
        time.sleep(7)

    startCounter += 1

    # WAIT FOR THE 'Q' BUTTON TO STOP
    if cv2.waitKey(1) & 0xFF == ord('q'):
        me.land()
        break

cv2.destroyAllWindows()