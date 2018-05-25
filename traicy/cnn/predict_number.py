import ImageFilter_noLoad
import CNN_load_model
import sys
import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont
from skimage import img_as_float


def draw_font(img, predicted_number, confidence, used_contour):
    x, y, w, h = cv2.boundingRect(used_contour)

    img = Image.fromarray(img)
    draw = ImageDraw.Draw(img)
    font = ImageFont.truetype("sans-serif.ttf", 16)
    draw.text((x+w-20, y+h-20), str(predicted_number), (255, 179, 0), font=font)

    img_np = np.array(img)

    ImageFilter_noLoad.save_image_with_drawn_chunks(img_np)


image_path = sys.argv[1]

if image_path is not None:
    # img_com = ImageFilter_noLoad.read_image_from_location(image_path)
    # img_flat = img_as_float(img_com.flatten().reshape(1, 784))

    # number, confidence = CNN_load_model.predict_image(img_flat)

    # print(str(number) + "," + str(confidence))

    img_list, contour_list, img_with_chunks = ImageFilter_noLoad.read_image_with_chunks_from_location(image_path)
    predictions = ""

    if len(img_list) == len(contour_list):
        for index in range(0, len(img_list)):

            image = img_list[index]
            contour = contour_list[index]

            img_flat = img_as_float(image.flatten().reshape(1, 784))

            number, confidence = CNN_load_model.predict_image(img_flat)
            draw_font(img_with_chunks, number, confidence, contour)

            predictions += (str(number) + ", " + str(confidence)) + "\n"

        print(predictions)
    else:
        raise Exception("the length of the image list and the contour list is not equal!")
