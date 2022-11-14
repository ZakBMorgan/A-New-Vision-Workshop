import cv2
import numpy as np

cap = cv2.VideoCapture(0)
title = 'Display - Press Esc to exit'
kernel = np.ones((5, 5), np.uint8)


def filter_contour(contour_input):
    min_area = 90000
    filteredContours = []
    for i in contour_input:
        area = cv2.contourArea(i)
        if area > min_area:
            filteredContours.append(i)
    return filteredContours


while True:
    ret, frame = cap.read()

    img = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    lower_blue = np.array([50, 18, 15])
    upper_blue = np.array([255, 255, 255])

    img = cv2.inRange(img, lower_blue, upper_blue)

    gray = cv2.Canny(img, 325, 790)
    gray = cv2.morphologyEx(gray, cv2.MORPH_GRADIENT, kernel)
    gray = cv2.dilate(gray, kernel, iterations=4)

    contours, hierarchy = cv2.findContours(gray, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    contours = filter_contour(contours)
    # cv2.drawContours(img, filter_contour(contours), -1, (0, 255, 0), 20)

    cv2.drawContours(img, contours, -1, color=(255, 255, 255), thickness=cv2.FILLED)

    new_frame = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)

    new_frame = cv2.bitwise_and(new_frame, frame)

    cv2.imshow(title, new_frame)
    key = cv2.waitKey(5)
    if key == 27:  # if ESC is pressed, exit
        cv2.destroyAllWindows()
        break
