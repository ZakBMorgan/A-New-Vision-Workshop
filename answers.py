from scv import *
import math

mode = 2
key = 0
expos = -8
alien_switch = False

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
    # "Cute Alien" is original artwork (Aric Volman)
    helmet = img_load('astro_helmet.png')  # Load the face
    alien = img_load('cute_alien.png')  # Load the cute alien
    while True:
        original = get_camera_image()  # Load the original image
        faces = find_faces(original)  # Find the mouths

        if len(faces) != 0:  # If there are mouths
            for i in range(0, len(faces)):
                x, y, width, height = faces[i]  # Get best match for mouth
                # print(height)
                offset_y = int(y - math.sqrt(height))  # Using the inverse square law
                offset_x = int(x - math.sqrt(width))  # Using the inverse square law
                if not alien_switch:
                    original = draw(original, helmet, offset_x, offset_y, int(width * 1.2), int(height * 1.2))
                if alien_switch:
                    original = draw(original, alien, offset_x, offset_y, int(width * 1.2), int(height * 1.2))

        key = show_image(original)

        if key == 97:  # A - Switches to and from Alien!
            # time.sleep(1)
            alien_switch = not alien_switch
        if key == 32:  # Space bar - Pauses
            time.sleep(10)

        if (expos <= -13):
            expos = -13
        if (expos >= -1):
            expos = -1

        if key == 122:  # Z key - Increase exposure
            expos += 1
            set_exposure(expos)

        if key == 120:  # X Key - Decrease exposure
            expos -= 1
            set_exposure(expos)
        if key == 27:  # if ESC is pressed, exit
            cv2.destroyAllWindows()
            break

