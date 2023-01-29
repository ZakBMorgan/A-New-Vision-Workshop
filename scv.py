import cv2
import time
import math

# Initializations
mouth_cascade = cv2.CascadeClassifier('mouth.xml')
face_cascade = cv2.CascadeClassifier('face.xml')

if mouth_cascade.empty():
    raise IOError('Unable to load the mouth cascade classifier xml file')

# Caffe DNN Initializations
# Using an older, pretrained model
# https://www.kaggle.com/datasets/sambitmukherjee/caffe-face-detector-opencv-pretrained-model
net = cv2.dnn.readNetFromCaffe('architecture.txt', 'weights.caffemodel')

# Title of window
title = 'Display - Press Z/X to change exposure, Press Space to pause, Esc to exit'

cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)

cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

# Sets window to full screen
cv2.namedWindow(title, cv2.WND_PROP_FULLSCREEN)
cv2.setWindowProperty(title, cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)


def img_load(img_path):
    """
    Wrapper for cv2.imread, because we don't want the kids to have to access OpenCV directly.
    """
    return cv2.imread(img_path, -1)  # Load the image with any alphas


def draw(l_img, s_img, x_offset, y_offset, width, height):
    """
    Draws s_image on top of l_image starting at an x and y offset from the top left corner of the image, and with the
    given width and height.
    """

    # Modified to scale from 360p to 1080p, to increase performance

    y_offset = 2 * int(y_offset - math.sqrt(height))  # Using the inverse square law
    x_offset = 2 * int(x_offset - math.sqrt(width))  # Using the inverse square law

    cv2.resize(l_img, (1920, 1080), interpolation=cv2.INTER_AREA)  # Resizes to 1080p

    s_img = cv2.resize(s_img, (int(2.5 * width), int(2.5 * height)),
                       interpolation=cv2.INTER_AREA)  # Resize overlay image

    # This Terrible Code was Copy Pasted Code from. OpenCV makes this really annoying but it works.:
    # http://stackoverflow.com/questions/14063070/overlay-a-smaller-image-on-a-larger-image-python-opencv

    # As of 1/15/2022 - Add error handling for this horrible code!

    for c in range(0, 3):
        try:
            l_img[y_offset:y_offset + s_img.shape[0], x_offset:x_offset + s_img.shape[1], c] = s_img[:, :, c] * (
                        s_img[:, :, 3] / 255.0) + l_img[y_offset:y_offset + s_img.shape[0],
                                                  x_offset:x_offset + s_img.shape[1], c] * (1.0 - s_img[:, :,
                                                                                                  3] / 255.0)
        except ValueError:
            return l_img
    return l_img  # Return the drawn over background image


def show_image(img):
    cv2.imshow(title, img)
    key = cv2.waitKey(1)
    return key


def get_height(img):
    return img.shape[0]


def get_width(img):
    return img.shape[1]


# Needed to detect faces with many shadows
def set_exposure(expos):
    cap.set(cv2.CAP_PROP_EXPOSURE, int(expos))


# TODO: FUNCTIONS

def get_camera_image():
    ret, frame = cap.read()
    return frame


def find_mouths(image):
    # Convert to grayscale and downscale to 360p
    gray = cv2.cvtColor(cv2.resize(image, (640, 360), interpolation=cv2.INTER_AREA), cv2.COLOR_BGR2GRAY)
    return mouth_cascade.detectMultiScale(gray, 1.7, 11)


def find_faces(image):
    # Convert to grayscale and downscale to 360p
    gray = cv2.cvtColor(cv2.resize(image, (640, 360), interpolation=cv2.INTER_AREA), cv2.COLOR_BGR2GRAY)
    return face_cascade.detectMultiScale(gray, 1.7, 1)


def find_faces_dnn(image):
    # Set an image input into DNN model
    net.setInput(cv2.dnn.blobFromImage(image, size=(300, 300), swapRB=True, crop=False))

    # Feed forward/calculate the output of the model
    netOut = net.forward()

    # For all detections
    for detection in netOut[0, 0, :, :]:
        width = (detection[5] - detection[3]) * 640
        height = (detection[6] - detection[4]) * 360
        x = detection[3] * 640
        y = detection[4] * 360
        return width, height, x, y
