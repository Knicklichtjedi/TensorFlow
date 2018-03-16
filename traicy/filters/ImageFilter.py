# scikit image
from skimage.feature import canny
from skimage.morphology import skeletonize
from skimage.io import imread, imsave
from skimage.transform import rotate
from skimage import img_as_ubyte
from skimage import img_as_uint
from skimage import filters as filters
# scipy
from scipy.ndimage import measurements
import numpy as np
# pillow
from PIL import Image
# exifread
import exifread
# os
import datetime
import os
import errno

"""Define image dimensions and postprocessing values"""
image_dimension = 28
image_dimension_small = 25

image_dimension_t = (image_dimension, image_dimension)
image_dimension_t_small = (image_dimension_small, image_dimension_small)

canny_strength = 0.5
binary_gaussian_strength = 0.5
binary_filter_threshold = 0.5


def create_canny_image(img_read, filename, folder):
    """
    Filters a given binary image array with the canny algorithm and saves it to a given location

    :parameter
        img_read: binary image array
        filename: name of the original image
        folder: directory of the new image

    :returns
        array filtered with canny algorithm
    """
    img_canny = canny(img_read, canny_strength)
    img_conv = img_as_ubyte(img_canny)

    imsave(folder + filename + '_' + 'canny' + '.png', img_conv)
    return img_canny


def create_skeleton_image(img_read, filename, folder):
    img_skeletonized = skeletonize(img_read)

    imsave(folder + filename + "_skeleton" + '.png', img_as_uint(img_skeletonized))

    return img_skeletonized


def create_binary_image(img_read, filename, folder):
    img_gaussian = filters.gaussian(img_read, binary_gaussian_strength)
    img_threshold = filters.threshold_mean(img_read)
    # img_threshold = 0.3333

    img_binary = img_gaussian < img_threshold

    imsave(folder + filename + "_binary" + '.png', img_as_uint(img_binary))

    return img_binary


def create_com_image(img_read, filename, folder):
    newfilename = folder + filename + '_centered.png'

    img_copy = np.zeros(image_dimension_t)

    center = measurements.center_of_mass(img_read)
    print(f"center of mass {center} in {img_read.shape}")

    row_counter = 0
    col_counter = 0

    true_positions_list = list()
    true_positions_list_moved = list()

    for pixel_row in img_read:
        for pixel_col in pixel_row:

            if pixel_col > binary_filter_threshold:
                true_positions_list.append((col_counter, row_counter))

            col_counter += 1
        col_counter = 0
        row_counter += 1

    x_movement = image_dimension / 2 - center[0]
    y_movement = image_dimension / 2 - center[1]

    # print(f"Moving image by {x_movement}, {y_movement}")

    for i in range(0, len(true_positions_list)):
        x_true = (true_positions_list[i])[1]
        y_true = (true_positions_list[i])[0]

        x_moved = round(x_true + x_movement)
        y_moved = round(y_true + y_movement)

        # print(f"Accessing {x_true}, {y_true} and moving to {x_moved}, {y_moved}")

        true_positions_list_moved.append((x_moved, y_moved))

    for element in true_positions_list_moved:
        max_dim = image_dimension - 1
        if element[0] > max_dim or element[1] > max_dim:
            print("DIMENSION WARNING")
        else:
            img_copy[int(element[0])][int(element[1])] = 1.0

    imsave(newfilename, img_copy)

    return img_copy


def create_scaled_image(img_read, filename, folder):
    newfilename = folder + filename + '_scaled.png'

    # y_dim, x_dim, rgb = img_read.shape
    #
    # print(f"Dimensions {x_dim}, {y_dim}")
    #
    # if x_dim > y_dim:
    #     scaling_factor = y_dim / image_dimension
    # else:
    #     scaling_factor = x_dim / image_dimension
    #
    # scaled_size = (round(x_dim / scaling_factor), round(y_dim / scaling_factor))
    #
    # print(f"Scaled Size: {scaled_size}")

    img_pil_array = Image.fromarray(img_read)

    img_cropped = img_pil_array.resize(image_dimension_t_small, Image.ANTIALIAS)
    img_cropped.save(newfilename, "PNG")

    return imread(newfilename, as_grey=True)


def create_folder(directory):
    try:
        os.makedirs(directory)
    except OSError as e:
        if e.errno != errno.EEXIST:
            raise


def get_image_rotation(filename):

    file = open(filename, 'rb')
    tags = exifread.process_file(file)

    for tag in tags.keys():
        if tag == 'Image Orientation':
            print(f"{tag}, value {tags[tag]}")
            return tags[tag]


def rotate_image(img_read, rotation):
    if rotation is not None:
        value_cw = -float((str.split(str(rotation), " ")[1]))
        img_rotated = rotate(img_read, value_cw)
        return img_rotated


def read_images():

    path = abspath(__file__ + "/../../")
    data_path = str(path) + "/data/"

    main_folder = data_path + "filtered/" + datetime.datetime.now().strftime("%Y_%m_%d_x_%H_%M_%S")
    create_folder(main_folder)

    for i in range(0, 10):
        filename = f"{i}.jpg"
        dir_name = data_path + "images_human_raw/" + filename

        sub_folder = main_folder + f"/{i}" + "/"
        create_folder(sub_folder)

        rotation = get_image_rotation(dir_name)
        img_reading = imread(dir_name, plugin='matplotlib')

        img_scaled = create_scaled_image(img_as_ubyte(img_reading), filename, sub_folder)

        img_rotated = rotate_image(img_scaled, rotation)
        img_binary = create_binary_image(img_rotated, filename, sub_folder)
        img_com = create_com_image(img_binary, filename, sub_folder)

        img_canny = create_canny_image(img_com, filename, sub_folder)
        img_skeleton = create_skeleton_image(img_com, filename, sub_folder)


def main():
    read_images()


if __name__ == "__main__":
    main()
