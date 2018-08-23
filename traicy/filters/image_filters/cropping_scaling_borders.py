import cv2
import numpy as np
from PIL import Image

from image_filters.binary_filters import clamp_float_values


def create_cropped_image(image, crop_border):
    """
    this method gives back a smaller image
    :param image: former image
    :param crop_border: size of border
    :return: cropped image
    """

    image_cropped = image[crop_border:-crop_border, crop_border:-crop_border]

    return image_cropped


def create_scaled_image(img_read, image_dimension):
    """
        Resize and change to aspect ratio of the image and save it to a given directory

        :parameter
            img_read: binary image array
            filename: name of the original image
            folder: directory of the new image

        :returns
            array of the scaled image
    """
    img_pil_array = img_read

    # resize using Pillow
    img_cropped = img_pil_array.resize(image_dimension)
    img_ndarray = np.array(img_cropped)

    img_ndarray = clamp_float_values(img_ndarray)

    return img_ndarray


def create_extended_chunk(image_chunk):
    """
    creates an extended image with equal width and height
    :param image_chunk: given image
    :return: new square image
    """
    h, w = image_chunk.shape

    if h > w:
        extension_range = int((h - w) / 2)

        image_container = np.zeros((h, h))

        for w_in_container in range(extension_range, extension_range + w):
            for h_in_container in range(0, h):
                image_container[h_in_container, w_in_container] = \
                    image_chunk[h_in_container, w_in_container - extension_range]

        return image_container

    elif w > h:
        extension_range = int((w - h) / 2)

        image_container = np.zeros((w, w))

        for w_in_container in range(0, w):
            for h_in_container in range(extension_range, extension_range + h):
                image_container[h_in_container, w_in_container] = \
                    image_chunk[h_in_container - extension_range, w_in_container]

        return image_container

    else:
        return image_chunk


def cropping(contours, img_pil, image_dimension):
    """
    goes through all contours and creates a list of images and saves them into a directory
    :param contours: list with contours
    :param img_pil: original image, called with PIL
    :param filename: filename of the image
    :param folder: foldername of the image
    :return: list with cropped and scaled images
    """

    cropped_list = list()  # list with cropped images

    # go through the list of contours
    for cnt in contours:
        x, y, w, h = cv2.boundingRect(cnt)  # get rectangle from contours
        cropped_image = img_pil.crop((x, y, x + w, y + h))  # get rectangle from image

        img_ndarray = np.array(cropped_image)
        img_extended = create_extended_chunk(img_ndarray)
        img_extended_pil = Image.fromarray(img_extended)
        img_scaled = create_scaled_image(img_extended_pil, image_dimension)


        cropped_list.append(img_scaled)  # save in list

    return cropped_list


def create_max_extended_image(image_chunk, image_dimension, image_dimension_t):
    """
    extends an image to the given dimensions
    :param image_chunk: original image
    :param image_dimension: dimension of the image
    :param image_dimension_t: dimension of the image as a tuple
    :return:
    """
    h, w = image_chunk.shape

    h_extension = image_dimension - h
    w_extension = image_dimension - w

    h_displacement = int(h_extension/2)
    w_displacement = int(w_extension/2)

    img_container = np.zeros(image_dimension_t)

    if h_extension >= 0 and w_extension >= 0:

        for h_index in range(h_displacement, h):
            for w_index in range(w_displacement, w):
                img_container[h_index, w_index] = image_chunk[h_index - h_displacement, w_index - w_displacement]

    return img_container


def create_borders(img_read, image_dimension, border_size):

    nd = img_read

    new_color = 0

    xrange = image_dimension

    for x in range(0, xrange):
        for y in range(0, border_size):
            nd[x, y] = new_color

        for y in range(xrange - border_size, xrange):
            nd[x, y] = new_color

    for y in range(0, xrange):
        for x in range(0, border_size):
            nd[x, y] = new_color

        for x in range(xrange - border_size, xrange):
            nd[x, y] = new_color

    return nd