from scv import *
import math

mode = 2
key = 0
expos = -8

# SUPER CHALLENGE # 1 ANSWER
if mode == 0:
    img = img_load('parlor.png')
    cone = img_load('cone.png')
    cream = img_load('greencircle.png')
    img = draw(img, cream, get_width(img) / 2 - 50, get_height(img) / 2 - 65, 100, 100)
    img = draw(img, cone, get_width(img) / 2 - 50, get_height(img) / 2, 100, 200)
    show_image(img)

# MOUTH DETECT AND DRAW CHALLENGE
elif mode == 1:
    original = img_load('face_detect.png')  # Load the original image
    faces = find_faces(original)  # Find the faces
    if len(faces) != 0:  # If there are faces
        x, y, width, height = faces[-1]  # Get best match for faces
        original = draw(original, img_load('greencircle.png'), x, y, width, height)
    show_image(original)

# MUSTACHE FINAL CHALLENGE ANSWER
elif mode == 2:
    # SPACE NIGHT - ASTRONAUT IMAGE adapted from: (Public Domain license)
    # https://freesvg.org/astronauts-helmet-vector-image
    stache = img_load('astro_helmet.png')  # Load the stache
    while True:
        original = get_camera_image()  # Load the original image
        faces = find_faces(original)  # Find the mouths

        if len(faces) != 0:  # If there are mouths
            for i in range(0, len(faces)):
                x, y, width, height = faces[i]  # Get best match for mouth
                # print(height)
                offset = int(y - math.sqrt(height))  # Using the inverse square law
                original = draw(original, stache, x, offset, int(width * 1.2), int(height * 1.2))

        key = show_image(original)
        if key == 32:
            time.sleep(5)
        if (expos <= -13):
            expos = -13
        if (expos >= -1):
            expos = -1

        if key == 122:
            expos += 1
            set_exposure(expos)

        if key == 120:
            expos -= 1
            set_exposure(expos)
        if key == 27:  # if ESC is pressed, exit
            cv2.destroyAllWindows()
            break

