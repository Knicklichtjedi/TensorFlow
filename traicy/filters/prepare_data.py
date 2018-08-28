from os.path import abspath
from skimage.io import imread, imsave
from skimage.color import rgb2gray
from skimage.filters import gaussian
import os
from skimage.util import img_as_float
import numpy as np
from skimage.morphology import skeletonize
from PIL import Image
from os.path import exists

# SET PATHS
from image_filter import assign_json_values, create_folder, save_image, image_dimension_t_small, image_dimension, \
    image_dimension_small, image_dimension_t, filter_binary_filter_threshold, image_border
from image_filters.binary_filters import clamp_binary_values
from image_filters.center_of_mass_and_fillout import create_com_image
from image_filters.cropping_scaling_borders import create_extended_chunk, create_scaled_image, create_max_extended_image

path = abspath(__file__ + "/../../")  # change directory to traicy
data_path_raw = path + "/data/data_cut/"  # read from folder
data_path_prepared_data = path + "/cnn/TRAICY_data/"
data_json_path = str(path) + "/configs/settings.json"

# SET CENTER OF MASS
center_of_mass_boolean = True

# SET SKELETON
skeleton_boolean = False


def main():
    """
    Starts data preparation.
    Converts image slices into valid training data.
    Warning: 63.648 files take a while to process!
    """
    assign_json_values(data_json_path)

    print("starting preparation.")

    file_list, labels_list = set_lists()
    # prepare data
    file_list_prepared, labels_list_prepared = prepare_image_data_list(file_list, labels_list,
                                                                       center_of_mass=center_of_mass_boolean,
                                                                       skeleton=skeleton_boolean)

    print("images are prepared.")

    # save data
    for index in range(0, len(file_list_prepared)):
        image = file_list_prepared[index]
        label = labels_list_prepared[index]

        prepared_image_path = data_path_prepared_data + label + "/"

        if not exists(prepared_image_path):
            create_folder(prepared_image_path)

        imsave(prepared_image_path + str(label) + "_" + str(index) + "_" + str(skeleton_boolean)
               + "_" + str(center_of_mass_boolean) + ".png", image)


def create_binary_image(image, gaussian_strength=0.5, threshold=0.775):
    """
    Creates an binary image via gaussian threshold comparision
    :param image: image to filter
    :param gaussian_strength: strength of the gaussian blur
    :param threshold: threshold when a pixel is white or black
    :return: binary image with values of 0 and 1
    """
    img_gaussian = gaussian(image, gaussian_strength)

    # Threshold comparison
    img_binary = img_as_float(img_gaussian < threshold)
    img_clamped = clamp_binary_values(img_binary)

    return img_clamped


def prepare_image(image, center_of_mass, skeleton):
    """
    Prepares an image to match the training format
    :param image: image to prepare
    :param center_of_mass: bool if center of mass should be used
    :param skeleton: bool if skeletonize should be used
    :return: prepared image
    """
    img_binary = create_binary_image(image)

    img_extended = create_extended_chunk(img_binary)

    img_pil = Image.fromarray(img_extended)
    img_scaled = create_scaled_image(img_pil, image_dimension_t_small)

    if center_of_mass:
        img_max_scale = create_com_image(img_scaled, image_dimension, image_dimension_t, image_dimension_small,
                                         filter_binary_filter_threshold, image_border)
    else:
        img_max_scale = create_max_extended_image(img_scaled, image_dimension, image_dimension_t)

    if skeleton:
        img_skeleton = img_as_float(skeletonize(img_max_scale))
    else:
        img_skeleton = np.copy(img_max_scale)

    return img_skeleton


def prepare_image_data_list(file_list, labels_list, center_of_mass=False, skeleton=False):
    """
    Starts data preparation for a list of images
    :param file_list: list of images to prepare
    :param labels_list: list of corresponding labels
    :param center_of_mass: bool if center of mass should be used
    :param skeleton: bool if skeletonize should be used
    :return: list of prepared images and list of labels
    """
    prepared_images = list()
    prepared_labels = list()

    for index in range(0, len(file_list)):
        prepared_image = prepare_image(file_list[index], center_of_mass, skeleton)

        print("image {} as {} has been prepared.".format(index, labels_list[index]))

        prepared_images.append(prepared_image)
        prepared_labels.append(labels_list[index])

    return prepared_images, prepared_labels


def set_lists():
    """
    Reads images from a directory with their folder names and returns them as lists
    :return: list of images and list of folder names that represent their labels
    """

    file_list = list()
    labels_list = list()

    # iterate over "labels"
    for letter_folder in os.listdir(data_path_raw):

        data_path_image_raw = data_path_raw + letter_folder + "/"

        # iterate over images per label
        for image_file in os.listdir(data_path_image_raw):

            img_conv = rgb2gray(imread(data_path_image_raw + image_file, plugin='matplotlib'))
            img_float = img_as_float(img_conv)

            file_list.append(img_float)
            labels_list.append(letter_folder)

    print("{} images were loaded with {} labels".format(len(file_list), len(labels_list)))

    return file_list, labels_list


if __name__ == "__main__":
    main()
