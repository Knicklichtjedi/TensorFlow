# scikit image
from skimage.morphology import skeletonize
from skimage.io import imread, imsave
import JSONSettings
# os
import datetime
import os
from os import listdir
from os.path import abspath
import errno

# Define image dimensions and postprocessing values
from image_filters.binary_filters import create_chromakey_image, clamp_binary_values
from image_filters.center_of_mass_and_fillout import create_fillout_image, create_com_image
from image_filters.contours import create_chunked_image
from image_filters.cropping_scaling_borders import create_scaled_image, create_cropped_image, create_borders
from image_filters.rotation import get_image_rotation_from_location, get_image_rotation, rotate_image

# image dimensions
image_dimension = 28
image_dimension_small = 27
image_dimension_t = (image_dimension, image_dimension)
image_dimension_t_small = (image_dimension_small, image_dimension_small)

# border thickness
image_border = 2
filter_chunk_border = 5

#filter strengths/threshold for canny & gaussian & fillout
filter_canny_strength = 0.5
filter_binary_gaussian_strength = 0.5
filter_fill_out_length = 2
filter_binary_filter_threshold = 0.5

#chromakey filter variables
filter_green_low = 50
filter_green_high = 170
filter_green_low_factor = filter_green_low / 360
filter_green_high_factor = filter_green_high / 360
filter_green_saturation = 0.5
filter_green_brightness = 0.25

#filenames
loading_possible_filename = list()

#minimal contours length for cv2.findContours()
filter_contours_length = 9000


def assign_json_values(filename_directory):
    """
    reads the JSON data and hands it over to the global variables.
    :param filename_directory: directory to read from
    """
    try:
        JSONSettings.parse_data(filename_directory)

        global image_dimension, image_dimension_small, image_border
        global filter_canny_strength, filter_binary_gaussian_strength, filter_binary_filter_threshold
        global filter_green_low, filter_green_high, filter_green_saturation, filter_green_brightness
        global loading_possible_filename
        global filter_contours_length, filter_fill_out_length, filter_chunk_border

        image_dimension = JSONSettings.get_data(JSONSettings.JSONValues.IMAGE_DIMENSION)
        image_dimension_small = JSONSettings.get_data(JSONSettings.JSONValues.IMAGE_DIMENSION_SMALL)
        image_border = JSONSettings.get_data(JSONSettings.JSONValues.IMAGE_BORDER)

        filter_canny_strength = JSONSettings.get_data(JSONSettings.JSONValues.FILTER_CANNY)
        filter_binary_gaussian_strength = JSONSettings.get_data(JSONSettings.JSONValues.FILTER_BIN_GAUSS)
        filter_binary_filter_threshold = JSONSettings.get_data(JSONSettings.JSONValues.FILTER_BIN_THRESHOLD)

        filter_green_low = JSONSettings.get_data(JSONSettings.JSONValues.FILTER_GREEN_LOW)
        filter_green_high = JSONSettings.get_data(JSONSettings.JSONValues.FILTER_GREEN_HIGH)

        filter_green_saturation = JSONSettings.get_data(JSONSettings.JSONValues.FILTER_GREEN_SATURATION)
        filter_green_brightness = JSONSettings.get_data(JSONSettings.JSONValues.FILTER_GREEN_BRIGHTNESS)

        loading_possible_filename = JSONSettings.get_data(JSONSettings.JSONValues.LOADING_POSSIBLE_FILENAME)

        filter_contours_length = JSONSettings.get_data(JSONSettings.JSONValues.FILTER_CONTOURS_LENGTH)

        filter_fill_out_length = JSONSettings.get_data(JSONSettings.JSONValues.FILTER_FILL_OUT_LENGTH)
        filter_chunk_border = JSONSettings.get_data(JSONSettings.JSONValues.FILTER_CHUNK_BORDER_STRENGTH)

        reassign_calculated_variables()

    except FileNotFoundError as e:
        # print(e.args)
        return


def reassign_calculated_variables():
    """
    calculates variables and passes them over to the globals
    :return:
    """

    global image_dimension, image_dimension_t, image_dimension_small, image_dimension_t_small
    global filter_green_low_factor, filter_green_high_factor, filter_green_low, filter_green_high

    image_dimension_t = (image_dimension, image_dimension)
    image_dimension_t_small = (image_dimension_small, image_dimension_small)

    filter_green_low_factor = filter_green_low / 360
    filter_green_high_factor = filter_green_high / 360


def save_image_with_drawn_chunks(img):
    """
    saves chunk from image in specific folder
    :param img: smaller image to save (chunk)
    """
    path = abspath(__file__ + "/../../")
    chunk_path = path + "/chunked/"
    filename = "chunked.png"

    create_folder(chunk_path)

    imsave(chunk_path + filename, img)


def save_image(img, filename, folder):
    """
    saves image in the given directory with the given name
    :param img: image to save
    :param filename: filename of the saved image
    :param folder: folder path
    """

    if filename is not None and folder is not None:
        strl = list()
        strl.append(folder)
        strl.append(filename)

        new_filename = ''.join(strl)

        imsave(new_filename, img)


def create_folder(directory):
    """
        Creates a new directory

        :parameter
            directory: Directory that has to be created
    """
    try:
        os.makedirs(directory)
    except OSError as e:
        if e.errno != errno.EEXIST:
            raise


def read_images_with_chunks():
    """

        Creates a new folder for the process with the necessary sub folder.
        Starts the filtering process for each image.
        Read -> Resize -> Rotate -> Binary -> CenterOfMass -> Canny + Skeleton

    """

    pre_border = 5

    #create path & filename
    path = abspath(__file__ + "/../../")
    data_path = str(path) + "/data/"
    json_path = str(path) + "/configs/settings.json"
    filename = "filtered.png"

    #json values
    assign_json_values(json_path)

    #create folder with time stamp
    main_folder = data_path + "filtered/" + datetime.datetime.now().strftime("%Y_%m_%d_x_%H_%M_%S")+"/"
    create_folder(main_folder)

    #path to readable files
    dir_name = data_path + "" + "images_green/"    # TODO
    directory_data = listdir(dir_name)

    #list of all loaded images
    loaded_images = list()

    #loads images
    for file in directory_data:
        file_ends_with = file.split(".")[-1].lower()

        if len(loading_possible_filename) > 0:
            for filename in loading_possible_filename:
                if file_ends_with == filename:
                    loaded_images.append(file)
                else:
                    pass
                    # print("Could not find file with: " + filename + " at " + file)

    list_of_return_images = list()
    list_of_return_contours = list()
    img_with_chunks = None

    for image_name in loaded_images:

        #assigns name of file to name of current image
        filename = image_name

        # read image
        img_reading = imread(dir_name + "/" + filename, plugin='matplotlib')

        # rotate image
        rotation = get_image_rotation(filename, dir_name)
        img_rotated = rotate_image(img_reading, rotation)

        h, w, c = img_rotated.shape
        img_with_chunks = img_rotated

        # img_rotated_gray = rgb2gray(img_rotated)

        # img_rotated_pil = Image.fromarray(img_rotated)
        # img_pre_crop = img_rotated_pil.crop((pre_border, pre_border, w - pre_border, h - pre_border))
        # img_np_pre_cropped = np.array(img_pre_crop)

        img_np_pre_cropped = create_cropped_image(img_rotated, pre_border)

        # create binary image
        img_binary = create_chromakey_image(img_np_pre_cropped, filter_green_low_factor, filter_green_high_factor, filter_green_saturation, filter_green_brightness)
        save_image(img_binary, filename + "_borders.png", main_folder)

        # Returned lists by chunking
        list_of_work_images, list_of_work_contours, img_with_chunks = create_chunked_image(img_binary, img_reading, filter_contours_length, filter_chunk_border, image_dimension_t_small)
        save_image(img_with_chunks, filename + "_chunk.png", main_folder)


        list_wi_length = len(list_of_work_images)
        list_wc_length = len(list_of_work_contours)

        if list_wi_length == list_wc_length:

            for index in range(list_wi_length):
                index_image = list_of_work_images[index]
                index_coord = list_of_work_contours[index]
                chunk_string = "___" + str(index) + "_chunk_"

                chunk_filename = filename + chunk_string


                # get binary image
                img_clamp = clamp_binary_values(index_image)
                save_image(img_clamp, chunk_filename + "_binary.png", main_folder)

                #schmiering
                img_fillout = create_fillout_image(img_clamp, filter_fill_out_length)
                save_image(img_fillout, chunk_filename + "_fillout.png", main_folder)

                # get black borders inside of image
                img_borders = create_borders(imread(main_folder + chunk_filename + "_fillout.png", plugin="matplotlib"), image_dimension_small, image_border)
                save_image(img_borders, chunk_filename + "_borders.png", main_folder)

                # create filtered images
                img_skeleton = skeletonize(img_borders)
                save_image(img_skeleton, chunk_filename + "_skeleton.png", main_folder)

                # align binary image to center of mass
                img_com = create_com_image(img_skeleton, image_dimension, image_dimension_t, image_dimension_small, filter_binary_filter_threshold, image_border)
                save_image(img_com, chunk_filename + "_com.png", main_folder)

                list_of_return_images.append(img_com)
                list_of_return_contours.append(index_coord)

    return list_of_return_images, list_of_return_contours, img_with_chunks


def read_image_with_chunks_from_location(directory):

    """
            Creates a new folder for the process with the necessary sub folder.
        Starts the filtering process for each image.
        Read -> Resize -> Rotate -> Binary -> CenterOfMass -> Canny + Skeleton
    :param directory: directory to read from
    :return:
    """

    path = abspath(__file__ + "/../../")
    json_path = str(path) + "/configs/settings.json"

    # get new json values and assign them
    assign_json_values(json_path)

    pre_border = 5

    list_of_return_images = list()
    list_of_return_contours = list()
    img_with_chunks = None

    data_path = path + "/filtered/"
    filename = "filtered.png"

    main_folder = data_path                                                                     # + "/ImageFilter" + "/"
    create_folder(main_folder)

    # read image
    img_reading = imread(directory, plugin='matplotlib')

    # rotate image
    rotation = get_image_rotation_from_location(directory)
    img_rotated = rotate_image(img_reading, rotation)

    img_with_chunks = img_rotated
    h, w, c = img_rotated.shape

    img_pre_crop = create_cropped_image(img_rotated, pre_border)

    # create binary image
    img_binary = create_chromakey_image(img_pre_crop, filter_green_low_factor, filter_green_high_factor, filter_green_saturation, filter_green_brightness)
    save_image(img_binary, filename + "_borders.png", main_folder)

    # Returned lists by chunking
    list_of_work_images, list_of_work_contours, img_with_chunks = create_chunked_image(img_binary, img_reading, filter_contours_length, filter_chunk_border, image_dimension_t_small)
    save_image(img_with_chunks, filename + "_chunk.png", main_folder)

    list_wi_length = len(list_of_work_images)
    list_wc_length = len(list_of_work_contours)

    if list_wi_length == list_wc_length:

        for index in range(list_wi_length):

            index_image = list_of_work_images[index]
            index_coord = list_of_work_contours[index]

            chunk_string = "___" + str(index) + "_chunk_"
            chunk_filename = filename + chunk_string

            # get binary image
            img_clamp = clamp_binary_values(index_image)

            img_fillout = create_fillout_image(img_clamp, filter_fill_out_length)
            save_image(img_fillout, chunk_filename + "_fillout.png", main_folder)

            # get black borders inside of image
            img_borders = create_borders(imread(main_folder + chunk_filename + "_fillout.png", plugin="matplotlib"), image_dimension_small, image_border)
            save_image(img_borders, chunk_filename + "_borders.png", main_folder)

            # create filtered images
            img_skeleton = skeletonize(img_borders)
            save_image(img_skeleton, chunk_filename + "_skeleton.png", main_folder)

            # align binary image to center of mass
            img_com = create_com_image(img_skeleton, image_dimension, image_dimension_t, image_dimension_small, filter_binary_filter_threshold, image_border)
            save_image(img_com, chunk_filename + "_com.png", main_folder)

            list_of_return_images.append(img_com)
            list_of_return_contours.append(index_coord)

        return list_of_return_images, list_of_return_contours, img_with_chunks


def main():
    """
    initialises method used to read from specific folder
    :return:
    """
    read_images_with_chunks()


if __name__ == "__main__":
    main()

