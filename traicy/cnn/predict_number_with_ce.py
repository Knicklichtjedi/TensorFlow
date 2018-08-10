import ImageFilter_noLoad
import NUMBER_load_model_with_fully_custom_estimator
import sys
import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont
from skimage.io import imsave
from os.path import abspath


def predict_images(img_list):
    predictions = ""
    predictions_list = list()

    for index in range(0, len(img_list)):
        image = img_list[index]

        path = abspath(__file__ + "/../../") + "/data/image_green/"
        imsave(path + "binary " + str(index) + ".png", image)

        img_to_predict = image.flatten().reshape(1, 784).astype(np.float32, copy=True)

        number, confidence = NUMBER_load_model_with_fully_custom_estimator.predict_image(img_to_predict)

        predictions += (str(number) + ", " + str(confidence)) + "\n"
        predictions_list.append((number, confidence))

    return predictions_list, predictions


def add_results_to_image(img_with_chunks, img_list, contour_list, predictions_list):
    y_s, x_s, c_s = img_with_chunks.shape

    pil_img = Image.new('RGB', (x_s, y_s), (0, 0, 0))
    draw = ImageDraw.Draw(pil_img)

    font = None
    try:
        # font = ImageFont.truetype("Raleway-Regular.ttf", 24)          # try to load raleway
        font = ImageFont.truetype("GOTHIC.TTF", 24)                     # try to load century gothic
    except OSError:
        pass

    if font is None:
        font = ImageFont.load_default().font

    for index in range(0, len(img_list)):
        contour_txt = contour_list[index]
        prediction = predictions_list[index]
        number_txt = prediction[0]
        confidence_txt = prediction[1]

        draw_font(number_txt, confidence_txt, contour_txt, draw, font)

    path = abspath(__file__ + "/../../") + "/data/image_green/"

    img_font = np.uint8(np.array(pil_img))

    img_combined = np.copy(img_with_chunks)
    y, x, c = img_combined.shape

    for y_i in range(0, y):
        for x_i in range(0, x):
            pixel_txt = img_font[y_i, x_i]

            if not is_pixel_black(pixel_txt):
                img_combined[y_i, x_i] = (1, 1, 1)
                pass

    # pil_img.save(path + "font_image_solo_font" + ".png")
    # imsave(path + "font_image_solo_chunk" + ".png", arr=np.copy(img_with_chunks))
    # imsave(path + "font_image_combined" + ".png", arr=img_combined)

    ImageFilter_noLoad.save_image_with_drawn_chunks(img_combined)


def is_pixel_black(pixel):
    is_black = False
    for i in range(0, len(pixel)):
        if pixel[i] == 0:
            is_black = True
        else:
            is_black = False
    return is_black


def draw_font(predicted_number, confidence_value, used_contour, draw, font):
    x, y, w, h = cv2.boundingRect(used_contour)
    formatted_confidence = "{:.2f}%".format(confidence_value * 100)

    draw.text((x + 10, y + h - 35), str(predicted_number) + "  |  " + str(formatted_confidence), fill=(255, 255, 255),
              font=font)


def main():
    if len(sys.argv) > 1:
        image_path = sys.argv[1]        # G:\Projekte\GitHub\TensorFlow\TensorFlow\traicy\data\image_green\test0.png
    else:
        raise Exception("No path was given via system arguments!")

    if image_path is not None:

        img_list, contour_list, img_with_chunks = ImageFilter_noLoad.read_image_with_chunks_from_location(image_path)

        if len(img_list) == len(contour_list):
            if len(img_list) == 0:
                raise Exception("No greenscreen result!")

            predictions_list, predictions = predict_images(img_list)
            add_results_to_image(img_with_chunks, img_list, contour_list, predictions_list)

            print(predictions)
        else:
            raise Exception("the length of the image list and the contour list is not equal!")


if __name__ == "__main__":
    main()