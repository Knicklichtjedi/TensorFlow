import image_filter
import NUMBER_load_model_with_fully_custom_estimator
import LETTER_load_model_with_fully_custom_estimator
import sys
import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont

letters = ["T", "R", "A", "I", "C", "Y"]    # possible results for formatting


def predict_images(img_list, model_mode):
    """
    Uses a list of images and a model identifier to predict numbers or letters in the list of images
    :param img_list: list of np.array images, shape 28x28
    :param model_mode: string "number" or "letter" as model identifier
    :return: list of prediction tuples (category, confidence) and formatted prediction string
    """
    predictions = ""
    predictions_list = list()

    for index in range(0, len(img_list)):
        image = img_list[index]

        # reshape image
        img_to_predict = image.flatten().reshape(1, 784).astype(np.float32, copy=True)

        if model_mode == "number":
            # predict
            number, confidence = NUMBER_load_model_with_fully_custom_estimator.predict_image(img_to_predict)

            predictions += "{}, {:.2f}\n".format(number, confidence * 100)
            predictions_list.append((number, confidence))
        elif model_mode == "letter":
            # predict
            number, confidence = LETTER_load_model_with_fully_custom_estimator.predict_image(img_to_predict)

            predictions += "{}, {:.2f}\n".format(letters[number], confidence * 100)
            predictions_list.append((letters[number], confidence))

    return predictions_list, predictions


def add_results_to_image(img_with_chunks, img_list, contour_list, predictions_list):
    """
    Draws results of the prediction on an image with chunks, category and confidence
    :param img_with_chunks: original image with has the chunks already drawn onto it
    :param img_list: list of images that were predicted
    :param contour_list: list of contours found in binary image
    :param predictions_list: list of predictions, includes category and confidence
    """
    y_s, x_s, c_s = img_with_chunks.shape

    pil_img = Image.new('RGB', (x_s, y_s), (0, 0, 0))
    draw = ImageDraw.Draw(pil_img)

    # load font
    font = None
    try:
        font = ImageFont.truetype("GOTHIC.TTF", 24)                     # try to load century gothic
    except OSError:
        print("")

    if font is None:
        font = ImageFont.load_default().font

    # extract data
    for index in range(0, len(img_list)):
        contour_txt = contour_list[index]
        prediction = predictions_list[index]
        number_txt = prediction[0]
        confidence_txt = prediction[1]

        draw_font(number_txt, confidence_txt, contour_txt, draw, font)

    img_font = np.uint8(np.array(pil_img))

    img_combined = np.copy(img_with_chunks)
    y, x, c = img_combined.shape

    # copy image onto img_with_chunks
    for y_i in range(0, y):
        for x_i in range(0, x):
            pixel_txt = img_font[y_i, x_i]

            if not is_pixel_black(pixel_txt):
                img_combined[y_i, x_i] = (1, 1, 1)
                pass

    # pil_img.save(path + "font_image_solo_font" + ".png")
    # imsave(path + "font_image_solo_chunk" + ".png", arr=np.copy(img_with_chunks))
    # imsave(path + "font_image_combined" + ".png", arr=img_combined)

    image_filter.save_image_with_drawn_chunks(img_combined)


def is_pixel_black(pixel):
    """
    Checks if a pixel element is black
    :param pixel: pixel element to be checked
    :return: Whether the pixel was black or not
    """
    is_black = False
    for i in range(0, len(pixel)):
        if pixel[i] == 0:
            is_black = True
        else:
            is_black = False
    return is_black


def draw_font(predicted_category, confidence_value, used_contour, draw, font):
    """
    Uses a PIL image handle to draw a formatted string on that handle
    :param predicted_category: the category that was predicted
    :param confidence_value: the confidence of the prediction of the category
    :param used_contour: contour of the current chunk
    :param draw: PIL image handle
    :param font: font to use for drawing
    """
    x, y, w, h = cv2.boundingRect(used_contour)
    formatted_confidence = "{:.2f}%".format(confidence_value * 100)

    draw.text((x + 10, y + h - 35), str(predicted_category) + "  |  " + str(formatted_confidence), fill=(255, 255, 255),
              font=font)


def main():
    """
    Extracts a file path for an image and a model identifier from launch arguments, starts image filtering on the
    image and if at least one contour is found it starts the prediction. In the end the prediction is printed so the C#
    GUI can receive it.
    """
    if len(sys.argv) > 2:
        image_path = sys.argv[1]        # G:\Projekte\GitHub\TensorFlow\TensorFlow\traicy\data\image_green\test0.png
        model_mode = sys.argv[2]
    else:
        image_path = None
        model_mode = "number"
        print("")

    if image_path is not None:

        img_list, contour_list, img_with_chunks = image_filter.read_image_with_chunks_from_location(image_path)

        if len(img_list) == len(contour_list):
            if len(img_list) == 0:
                print("")

            predictions_list, predictions = predict_images(img_list, model_mode)
            add_results_to_image(img_with_chunks, img_list, contour_list, predictions_list)

            print(predictions)
        else:
            print("")


if __name__ == "__main__":
    main()
