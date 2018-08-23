import cv2
import numpy as np
from scipy.ndimage import measurements
from skimage import img_as_ubyte, img_as_uint
from skimage.color import rgb2gray
from skimage.morphology import skeletonize


def create_com_image(img_read, image_dimension, image_dimension_t, image_dimension_small, binary_threshold, image_border):
    """
        Calculates the center of mass of all white pixels and moves them towards it

        :parameter
            img_read: binary image array
            filename: name of the original image
            folder: directory of the new image

        :returns
            array of the new centered image
    """

    img_copy = np.zeros(image_dimension_t)

    # Calculate center of mass
    center = measurements.center_of_mass(img_read)

    row_counter = 0
    col_counter = 0

    true_positions_list = list()
    true_positions_list_moved = list()

    # find all pixels with a value greater than binary_filter_threshold
    # In most cases the pixels will only have values of 0 or 1
    for pixel_row in rgb2gray(img_read):
        for pixel_col in pixel_row:

            if pixel_col > binary_threshold:
                # add pixel position in array to list
                true_positions_list.append((col_counter, row_counter))

            col_counter += 1
        col_counter = 0
        row_counter += 1

    # calculate pixel shifting for center of mass
    x_movement = image_dimension / 2 - center[0]
    y_movement = image_dimension / 2 - center[1]

    # move pixels that were over the threshold
    for i in range(0, len(true_positions_list)):
        x_true = (true_positions_list[i])[1]
        y_true = (true_positions_list[i])[0]

        x_moved = round(x_true + x_movement)
        y_moved = round(y_true + y_movement)

        # Create a border around the image before centering it

        if (image_border - 1 < x_moved < image_dimension_small - image_border) \
                and (image_border - 1 < y_moved < image_dimension_small - image_border):
            true_positions_list_moved.append((x_moved, y_moved))

    #  Check if new pixel position is outside of the array dimensions
    for element in true_positions_list_moved:
        max_dim = image_dimension - 1
        if element[0] > max_dim or element[1] > max_dim:
            continue
        else:
            img_copy[int(element[0])][int(element[1])] = 1.0

    return img_copy


def create_fillout_image(img_read, fillout_length):
    """
        Iterates 4 times over the image-array and adds white pixels after every last white pixel inside the image
        The form of an object will mostly be kept or even stabilised
        At half the iterations the image will be transposed so rotating should happen afterwards maybe

        :parameter
            img_read: binary image array
            filename: name of the original image
            folder: directory of the new image

        :returns
            array of the new binary image
    """
    last_white = False

    it = fillout_length

    test = np.array(img_read)

    for i in range(it):

        if i != 1:
            for row in test:
                for col in range(len(row)):

                    if row[col] > 0:

                        row[col] = 1

                        last_white = True
                    elif row[col] < 1 and last_white:
                        row[col] = 1

                        last_white = False
                    else:
                        row[col] = 0

                last_white = False
        else:
            test = cv2.transpose(test)

    test = cv2.transpose(test)

    return img_as_uint(test)
