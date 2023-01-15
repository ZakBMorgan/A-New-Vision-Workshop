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

    lower_blue = np.array([10, 18, 15])
    # upper_blue = np.array([255, 255, 255])
    upper_blue = np.array([235, 235, 235])

    img = cv2.inRange(img, lower_blue, upper_blue)

    # gray = cv2.Canny(img, 325, 790)
    gray = cv2.Canny(img, 200, 200)
    gray = cv2.morphologyEx(gray, cv2.MORPH_GRADIENT, kernel)
    gray = cv2.dilate(gray, kernel, iterations=3)

    contours, hierarchy = cv2.findContours(gray, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    contours = filter_contour(contours)

    cv2.drawContours(img, contours, -1, color=(255, 255, 255), thickness=cv2.FILLED)

    final = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)
    final = cv2.bitwise_not(final)  # If contours are drawn incorrectly
    final = cv2.bitwise_and(final, frame)

    cv2.imshow(title, final)
    key = cv2.waitKey(5)
    if key == 27:  # if ESC is pressed, exit
        cv2.destroyAllWindows()
        break
