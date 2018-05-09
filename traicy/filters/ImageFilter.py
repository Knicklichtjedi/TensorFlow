# scikit image
from skimage.feature import canny
from skimage.morphology import skeletonize
from skimage.io import imread, imsave
from skimage.transform import rotate
from skimage import img_as_ubyte
from skimage import img_as_uint
from skimage import filters as filters
from skimage.color import rgb2hsv, hsv2rgb, rgb2gray
# openCV
import cv2
# scipy
from scipy.ndimage import measurements
import numpy as np
# pillow
from PIL import Image
# exifread
import exifread
#custom modules
import JSONSettings
# os
import datetime
import os
from os.path import abspath
import errno

# Define image dimensions and postprocessing values
image_dimension = 28
image_dimension_small = 27

image_border = 2

image_dimension_t = (image_dimension, image_dimension)
image_dimension_t_small = (image_dimension_small, image_dimension_small)

filter_canny_strength = 0.5
filter_binary_gaussian_strength = 0.5
filter_binary_filter_threshold = 0.5

filter_green_low = 50
filter_green_high = 180

filter_green_low_factor = filter_green_low / 360
filter_green_high_factor = filter_green_high / 360

filter_green_saturation = 0.5
filter_green_brightness = 0.75

filter_contours_length = 500


def assign_json_values(filename_directory):
    try:
        JSONSettings.parse_data(filename_directory)

        global image_dimension, image_dimension_small, image_border
        global filter_canny_strength, filter_binary_gaussian_strength, filter_binary_filter_threshold
        global filter_green_low, filter_green_high, filter_green_saturation, filter_green_brightness
        global filter_contours_length

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

        filter_contours_length = JSONSettings.get_data(JSONSettings.JSONValues.FILTER_CONTOURS_LENGTH)

        reassign_calculated_variables()

    except errno:
        # TODO Error message
        return



def reassign_calculated_variables():

    global image_dimension, image_dimension_t, image_dimension_small, image_dimension_t_small
    global filter_green_low_factor, filter_green_high_factor, filter_green_low, filter_green_high

    image_dimension_t = (image_dimension, image_dimension)
    image_dimension_t_small = (image_dimension_small, image_dimension_small)

    filter_green_low_factor = filter_green_low / 360
    filter_green_high_factor = filter_green_high / 360


def create_chunked_image(img_binary, filename, folder):
    """
    gets every outline in the image and creates images with the biggest ones (according to the theshold filter_contours_length)
    :param img_binary: large image, not chunked yet
    :param filename: name of the image
    :param folder: location of the image
    :return: a list of chunks (smaller images) and a second list with their location in the big image
    """


    img_binary_cv2 = cv2.imread(folder + filename + '_' + 'binary' + '.png') #loads image with cv2 standarts

    thresh = img_as_ubyte(img_binary) #loads image as ubyte

    #finds the contours and gives back the original picture and a hierarchy of the contours
    im2, contours, hierarchy = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    count = 0 #count contours that fit the threshold
    beste = [] #save contours in a list
    for cnt in contours:
        if cv2.contourArea(cnt) > filter_contours_length:
            beste.append(cnt)

    #how many contours were found?
    print (len(beste))

    #open Image with PIL
    img_binary_PIL = Image.open(folder + filename + '_' + 'binary' + '.png')

    img_with_chunks = draw_chunks(img_binary_cv2, beste) #draw Chunks at original image
    imsave(folder + filename + '_' + 'chunked' + '.png', img_with_chunks) #save image with drawn chunks

    #crop image
    cropped_images = crop(img_binary_cv2, beste, img_binary_PIL, filename, folder)


    return cropped_images, beste


def crop(contours, img_PIL, filename, folder):
    """
    goes through all contours and creates a list of images
    :param contours: list with contours
    :param img_PIL: original image, called with PIL
    :param filename: filename of the image
    :param folder: foldername of the image
    :return: list with cropped and scaled images
    """

    cropped_list = list()#list with cropped images

    # go through the list of contours
    for cnt in contours:
        x, y, w, h = cv2.boundingRect(cnt) # get rectangle from contours
        cropped_image = img_PIL.crop((x,y,w,h)) # get rectangle from image
        img_scaled = create_scaled_image(cropped_image, folder, filename) # scale image to 27x27 size
        cropped_list.append(img_scaled) # save in list

    return cropped_list


def clamp_binary_values(img):
    """
    creates np array from image
    :param img: original image
    :return: np array
    """
    img_np_array = rgb2gray(np.array(img))
    h, w = img_np_array.shape

    for x in range(0, w):
        for y in range(0, h):
            if img_np_array[y, x] > 0:
                img_np_array[y, x] = 1

    return img_np_array

def draw_chunks(img, contours):
    """
    draws chunks in color green on the original image
    :param img: original image
    :param contours: list of contours
    :return: image with contours
    """
    for a in contours:
        x, y, w, h = cv2.boundingRect(a)
        cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)

    return img



def create_bordered_image(img_read, filename, folder):
    """
    filters the borders of the image in a specific border size to black
    :param img_read: binary image array
    :param filename: name of the original image
    :param folder: directory of the new image
    :return: image with black borders
    """
    # nd = imread(folder + filename + '_binary.png')
    nd = img_read
    newfilename = folder + filename + '_borders.png'
    new_color = 0

    xrange = image_dimension_small

    for x in range(0, xrange):
        for y in range(0, image_border):
            nd[x, y] = new_color

        for y in range(xrange - image_border, xrange):
            nd[x, y] = new_color

    for y in range(0, xrange):
        for x in range(0, image_border):
            nd[x, y] = new_color

        for x in range(xrange - image_border, xrange):
            nd[x, y] = new_color

    imsave(newfilename, nd)
    return nd


def create_canny_image(img_read, filename, folder):
    """
    Filters a given binary image array with the canny algorithm and saves it to a given directory

    :parameter
        img_read: binary image array
        filename: name of the original image
        folder: directory of the new image

    :returns
        array filtered with canny algorithm
    """
    img_canny = canny(img_read, filter_canny_strength)
    img_conv = img_as_ubyte(img_canny)

    imsave(folder + filename + '_' + 'canny' + '.png', img_conv)
    return img_canny


def create_skeleton_image(img_read, filename, folder):
    """
    Uses a binary image and creates a skeleton of it and saves it to a given directory

    :parameter
        img_read: binary image array
        filename: name of the original image
        folder: directory of the new image

    :returns
        array of binary image as skeleton
    """
    img_skeletonized = skeletonize(img_read)

    imsave(folder + filename + "_skeleton" + '.png', img_as_uint(img_skeletonized))

    return img_skeletonized


def create_binary_image(img_read, filename, folder):
    """
        Converts a given image into a binary image via threshold comparison and saves it to a given directory

        :parameter
            img_read: binary image array
            filename: name of the original image
            folder: directory of the new image

        :returns
            array of the new binary image
    """
    img_conv = rgb2gray(img_read)

    img_gaussian = filters.gaussian(img_conv, filter_binary_gaussian_strength)
    img_threshold = filters.threshold_mean(img_conv)

    # Threshold comparison
    img_binary = img_gaussian < img_threshold

    imsave(folder + filename + "_binary" + '.png', img_as_uint(img_binary))

    return img_binary


def create_greenfiltered_image(img_read, filename, folder):

    icol = (36, 202, 59, 76, 255, 255)  # green

    frame = img_read
    #  cv2.imshow('frame', frame)

    lowHue = icol[0]
    lowSat = icol[1]
    lowVal = icol[2]
    highHue = icol[3]
    highSat = icol[4]
    highVal = icol[5]

    # frameBGR = cv2.GaussianBlur(frame, (7, 7), 0)
    #  cv2.imshow('blurred', frameBGR)

    # img_np = np.copy(frameBGR)
    # img_conv = img_np.astype(np.uint16)
    img_hsv = rgb2hsv(frame)
    # img_shape = img_hsv.reshape()

    imsave(folder + filename + "_binary_hsv" + '.png', hsv2rgb(img_hsv))

    for pixel_row in img_hsv:
        for pixel_col in pixel_row:
            pixel_col[0] *= 180
            pixel_col[1] *= 255
            pixel_col[2] *= 255

    # hsv = cv2.cvtColor(img_conv, cv2.COLOR_BGR2HSV)
    colorLow = np.array([lowHue, lowSat, lowVal])
    colorHigh = np.array([highHue, highSat, highVal])
    mask = cv2.inRange(img_hsv, colorLow, colorHigh)

    mask2 = cv2.inRange
    #  cv2.imshow('mask-plain', mask)

    kernal = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (9, 9))
    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernal)
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernal)
    #  cv2.imshow('mask', mask)

    mask_inv = cv2.bitwise_not(mask)
    #  cv2.imshow('mask_inv', mask_inv)

    imsave(folder + filename + "_binary" + '.png', img_as_uint(mask_inv))

    return imread(folder + filename + "_binary" + '.png', as_grey=True)


def create_chromakey_image(img_read, filename, folder):


    hsv = rgb2hsv(img_read)

    for pixel_row in hsv:
        for pixel_col in pixel_row:

            if filter_green_low_factor < pixel_col[0] <= filter_green_high_factor:
                    # and pixel_col[1] > filter_green_saturation \
                    # and pixel_col[2] < filter_green_brightness:

                pixel_col[0] = 0
                pixel_col[1] = 0
                pixel_col[2] = 0
            else:

                pixel_col[0] = 1
                pixel_col[1] = 1
                pixel_col[2] = 1

    imsave(folder + filename + '_' + 'binary' + '.png', hsv)

    return imread(folder + filename + '_' + 'binary' + '.png', as_grey=True)


def create_com_image(img_read, filename, folder):
    """
        Calculates the center of mass of all white pixels and moves them towards it and saves it to a given directory

        :parameter
            img_read: binary image array
            filename: name of the original image
            folder: directory of the new image

        :returns
            array of the new centered image
    """

    new_filename = folder + filename + '_centered.png'

    img_copy = np.zeros(image_dimension_t)

    # Calculate center of mass
    center = measurements.center_of_mass(img_read)
    # print(f"center of mass {center} in {img_read.shape}")

    row_counter = 0
    col_counter = 0

    true_positions_list = list()
    true_positions_list_moved = list()

    # find all pixels with a value greater than binary_filter_threshold
    # In most cases the pixels will only have values of 0 or 1
    for pixel_row in rgb2gray(img_read):
        for pixel_col in pixel_row:

            if pixel_col > filter_binary_filter_threshold:
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
            # print("DIMENSION WARNING")
            continue
        else:
            img_copy[int(element[0])][int(element[1])] = 1.0

    imsave(new_filename, img_copy)

    return img_copy


def create_scaled_image(img_read, folder, filename):
    """
        Resize and change to aspect ratio of the image and save it to a given directory

        :parameter
            img_read: binary image array
            filename: name of the original image
            folder: directory of the new image

        :returns
            array of the scaled image
    """
    newfilename = folder + filename + '_scaled.png'

    # OLD CODE : USE IF IMAGE HAS TO KEEP ITS ASPECT RATIO
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

    img_pil_array = img_read

    # resize using Pillow
    img_cropped = img_pil_array.resize(image_dimension_t_small, Image.ANTIALIAS)
    img_cropped.save(newfilename, "PNG")

    # reload image due to pillow using its own image class
    return imread(newfilename)


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


def get_image_rotation(filename):
    """
        Get the Image Orientation Tag from an image and return it

        :parameter
            filename: name of the original image

        :returns
            EXIF file tag if it exists
    """

    file = open(filename, 'rb')
    tags = exifread.process_file(file)

    for tag in tags.keys():
        if tag == 'Image Orientation':
            # print(f"{tag}, value {tags[tag]}")
            return tags[tag]


def rotate_image(img_read, rotation):
    """
        Rotates a given image by a given rotation clock wise

        :parameter
            img_read: binary image array
            rotation: Rotation clock wise in degree

        :returns
            array of the new rotated image
    """
    if rotation is not None:
        value_cw = -float((str.split(str(rotation), " ")[1]))
        img_rotated = rotate(img_read, value_cw)
        return img_rotated
    else:
        return img_read



def read_images_with_chunks():
    """
        Creates a new folder for the process with the necessary sub folder.
        Starts the filtering process for each image.
        Read -> Rotate -> Binary -> Chunking -> CenterOfMass -> Canny + Skeleton

    """

    path = abspath(__file__ + "/../../")
    data_path = str(path) + "/data/"
    json_path = str(path) + "/configs/settings.json"

    assign_json_values(json_path)

    print(filter_contours_length)

    main_folder = data_path + "filtered/" + datetime.datetime.now().strftime("%Y_%m_%d_x_%H_%M_%S")
    create_folder(main_folder)

    for i in range(0, 4):
        filename = f"{i}.png"
        dir_name = data_path + "images_nice_green/" + filename

        # create folder and sub folder
        sub_folder = main_folder + f"/{i}" + "/"
        create_folder(sub_folder)

        # get rotation of image and read it
        rotation = get_image_rotation(dir_name)
        img_reading = imread(dir_name, plugin='matplotlib')

        # rotate image
        img_rotated = rotate_image(img_reading, rotation)

        # create binary image
        #img_binary = create_binary_image(img_rotated, filename, sub_folder)
        # img_binary = create_greenfiltered_image(img_rotated, filename, sub_folder)
        img_binary = create_chromakey_image(img_rotated, filename, sub_folder)

        #get a list of chunks and a list where these chunks are in the big image
        img_chunk, img_coord = create_chunked_image(img_binary, filename, sub_folder)

        # for image in img_chunk:
        #     img_clamped = clamp_binary_values(image)
        #     imsave(img_clamped, filename + "_clamped.jpg", sub_folder)

        # get black borders inside of image
        #img_borders = create_bordered_image(img_chunk, filename, sub_folder)

        # create two filtered images
        # img_canny = create_canny_image(img_borders, filename, sub_folder)   # UNUSED!
        #img_skeleton = create_skeleton_image(img_borders, filename, sub_folder)

        # align binary image to center of mass
        #img_com = create_com_image(img_skeleton, filename, sub_folder)


def read_image_from_location(directory):

    path = abspath(__file__ + "/../../")
    json_path = str(path) + "/configs/settings.json"

    # get new json values and assign them
    assign_json_values(json_path)

    data_path = path + "/filtered/"
    filename = "filtered.png"

    main_folder = data_path + datetime.datetime.now().strftime("%Y_%m_%d_x_%H_%M_%S") + "/"
    create_folder(main_folder)

    # get rotation of image and read it
    rotation = get_image_rotation(directory)
    img_reading = imread(directory, plugin='matplotlib')

    # resize image
    img_scaled = create_scaled_image(img_as_ubyte(img_reading), filename, main_folder)

    # rotate image
    img_rotated = rotate_image(img_scaled, rotation)

    # create binary image
    img_binary = create_chromakey_image(img_rotated, filename, main_folder)

    # get black borders inside of image
    img_borders = create_bordered_image(img_binary, filename, main_folder)

    # create filtered images
    img_skeleton = create_skeleton_image(img_borders, filename, main_folder)

    # align binary image to center of mass
    img_com = create_com_image(img_skeleton, filename, main_folder)

    return img_com


def main():
    read_images_with_chunks()


if __name__ == "__main__":
    main()
