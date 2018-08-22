import cv2
import numpy as np
from PIL import Image
from skimage import img_as_ubyte, img_as_float

from image_filters.cropping_scaling_borders import cropping


def draw_rectangle(x, y, w, h, picture, chunk_border):

    color = (255 / 255, 179 / 255, 0)

    for contour_strength in range(0, chunk_border):
        for height in range(y, y + h):
            picture[height, x + contour_strength] = color
            picture[height, x + w - contour_strength] = color
        for width in range(x + contour_strength, x + w - contour_strength):
            picture[y + contour_strength, width] = color
            picture[y + h - contour_strength, width] = color


def create_chunked_image(img_binary, original_image, contours_length, border_size, image_dimension):
    """
    gets every outline in the image and creates images with the biggest ones
    (according to the threshold filter_contours_length)
    :param img_binary: large image, not chunked yet
    :param filename: name of the image
    :param folder: location of the image
    :param original_image: original image
    :return: a list of chunks (smaller images) and a second list with their location in the big image
    """

    thresh = img_as_ubyte(img_binary)  # loads image as ubyte

    # finds the contours and gives back the original picture and a hierarchy of the contours
    im2, contours, hierarchy = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    best_contours = []   # save contours in a list
    for cnt in contours:
        if cv2.contourArea(cnt) > contours_length:
            best_contours.append(cnt)

    # open Image with PIL
    img_binary_pil = Image.fromarray(img_binary)

    img_with_chunks = img_as_float(np.copy(original_image))   # draw Chunks at original image

    if best_contours:

        for image_index in range(len(best_contours)):

            x, y, w, h = cv2.boundingRect(best_contours[image_index])

            draw_rectangle(x, y, w, h, img_with_chunks, border_size)

    # crop image
    cropped_images = cropping(best_contours, img_binary_pil, image_dimension)

    return cropped_images, best_contours, img_with_chunks


def draw_red_rectangle(x, y, w, h, picture, chunk_border):

    color = (1, 0, 0)

    for contour_strength in range(0, chunk_border):
        for height in range(y, y + h):
            picture[height, x + contour_strength] = color
            picture[height, x + w - contour_strength] = color
        for width in range(x + contour_strength, x + w - contour_strength):
            picture[y + contour_strength, width] = color
            picture[y + h - contour_strength, width] = color
