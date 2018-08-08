# scikit image
from skimage.feature import canny
from skimage.morphology import skeletonize
from skimage.io import imread, imsave
from skimage.transform import rotate
from skimage import img_as_ubyte, img_as_uint, img_as_float
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
from os import listdir
from os.path import abspath
import errno
import time
import matplotlib

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
filter_green_high = 170

filter_green_low_factor = filter_green_low / 360
filter_green_high_factor = filter_green_high / 360

filter_green_saturation = 0.5
filter_green_brightness = 0.25

loading_possible_filename = list()

filter_contours_length = 9000

filter_fill_out_length = 2
filter_chunk_border = 5


def assign_json_values(filename_directory):
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

    global image_dimension, image_dimension_t, image_dimension_small, image_dimension_t_small
    global filter_green_low_factor, filter_green_high_factor, filter_green_low, filter_green_high

    image_dimension_t = (image_dimension, image_dimension)
    image_dimension_t_small = (image_dimension_small, image_dimension_small)

    filter_green_low_factor = filter_green_low / 360
    filter_green_high_factor = filter_green_high / 360


def save_image_with_drawn_chunks(img):
    path = abspath(__file__ + "/../../")
    chunk_path = path + "/chunked/"
    filename = "chunked.png"

    create_folder(chunk_path)

    imsave(chunk_path + filename, img)


def create_borders(img_read, filename, folder):

    # nd = imread(folder + filename + '_binary.png')
    nd = img_read

    new_name = '_borders.png'

    strl = list()
    strl.append(folder)
    strl.append(filename)
    strl.append(new_name)

    newfilename = ''.join(strl)

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

    strl = list()
    strl.append(folder)
    strl.append(filename)
    strl.append('_canny.png')

    new_filename = ''.join(strl)

    imsave(new_filename, img_conv)

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

    strl = list()
    strl.append(folder)
    strl.append(filename)
    strl.append('_skeleton.png')

    new_filename = ''.join(strl)

    imsave(new_filename, img_as_uint(img_skeletonized))

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

    strl = list()
    strl.append(folder)
    strl.append(filename)
    strl.append('_binary.png')

    new_filename = ''.join(strl)

    imsave(new_filename, img_as_uint(img_binary))

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

    strl = list()
    strl.append(folder)
    strl.append(filename)
    strl.append('_binary_hsv.png')

    new_filename = ''.join(strl)

    imsave(new_filename, hsv2rgb(img_hsv))

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

    strl_2 = list()
    strl_2.append(folder)
    strl_2.append(filename)
    strl_2.append('_binary.png')

    new_filename_2 = ''.join(strl_2)

    imsave(new_filename_2, img_as_uint(mask_inv))

    img_ndarray = np.array(img_as_uint(mask_inv))
    img_gray = rgb2gray(hsv2rgb(img_ndarray))

    # return imread(folder + filename + "_binary" + '.png', as_grey=True)
    return img_gray


def create_fillout_image(img_read, filename, folder):
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
    lastWhite = False

    it = filter_fill_out_length

    test = np.array(img_read)

    for i in range(it):

        if i != 1:
            #print(i)
            for row in test:
                for col in range(len(row)):

                    if row[col] > 0:


                        row[col] = 1

                        lastWhite = True
                    elif row[col] < 1 and lastWhite == True:
                        # print('black append')
                        row[col] = 1

                        lastWhite = False
                    else:
                        row[col] = 0
                        # print('black')


                lastWhite = False
        else:
            test = cv2.transpose(test)

    test = cv2.transpose(test)

    imsave(folder + filename + "_fillout" + '.png', img_as_uint(test))

    return imread(folder + filename + "_fillout" + '.png', plugin="matplotlib")


def create_chromakey_image(img_read, filename, folder):
    hsv = rgb2hsv(img_read)

    imsave(folder + filename + "_pre_chromakey.png", hsv)

    for pixel_row in hsv:
        for pixel_col in pixel_row:

            if filter_green_low_factor < pixel_col[0] <= filter_green_high_factor \
                    and pixel_col[1] > filter_green_saturation \
                    and pixel_col[2] > filter_green_brightness:

                pixel_col[0] = 0
                pixel_col[1] = 0
                pixel_col[2] = 0
            else:

                pixel_col[0] = 1
                pixel_col[1] = 1
                pixel_col[2] = 1

    imsave(folder + filename + "_post_chromakey.png", hsv)

    img_ndarray = np.array(hsv)
    img_rgb = hsv2rgb(img_ndarray)

    img_gray = rgb2gray(img_rgb)
    img_gray_copy = np.copy(img_gray)

    x, y = img_gray_copy.shape

    for i in range(0, x):
        for j in range(0, y):
            pixel = img_gray_copy[i, j]
            if pixel > 0:
                img_gray_copy[i, j] = 1
            else:
                img_gray_copy[i, j] = 0

    strl = list()
    strl.append(folder)
    strl.append(filename)
    strl.append('_binary.png')

    new_filename = ''.join(strl)

    imsave(new_filename, img_gray_copy)

    # return imread(folder + filename + '_' + 'binary' + '.png', as_grey=True)
    return img_gray_copy


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


def create_chunked_image(img_binary, filename, folder, originalImage):
    """
    gets every outline in the image and creates images with the biggest ones (according to the theshold filter_contours_length)
    :param img_binary: large image, not chunked yet
    :param filename: name of the image
    :param folder: location of the image
    :return: a list of chunks (smaller images) and a second list with their location in the big image
    """




    thresh = img_as_ubyte(img_binary) # loads image as ubyte

    # finds the contours and gives back the original picture and a hierarchy of the contours
    im2, contours, hierarchy = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    count = 0   # count contours that fit the threshold


    best_contours = []   # save contours in a list
    for cnt in contours:
        if cv2.contourArea(cnt) > filter_contours_length:
            #cv2.drawContours(img_with_chunks, [cnt], 0, (255, 179, 0), 3)
            #cv2.rectangle(img_with_chunks, (x,y), (w,h), (255, 0, 0), 2)
            best_contours.append(cnt)
    # how many contours were found?
    # print (len(best_contours))


    # open Image with PIL
    img_binary_PIL = Image.fromarray(img_binary)
    #save image with drawn chunks

    img_with_chunks = img_as_float(np.copy(originalImage))#draw Chunks at original image

    if best_contours:

        for image_index in range(len(best_contours)):

            x, y, w, h = cv2.boundingRect(best_contours[image_index])

            draw_rectangle(x, y, w, h, img_with_chunks, filter_chunk_border)

    save_image_with_drawn_chunks(img_with_chunks)
    # crop image
    cropped_images = cropping(best_contours, img_binary_PIL, filename, folder)

    return cropped_images, best_contours, img_with_chunks


def draw_rectangle(x, y, w, h, picture, chunk_border):

    color = (255 / 255, 179 / 255, 0)

    for contour_strength in range(0, chunk_border):
        for height in range(y, y + h):
            picture[height, x + contour_strength] = color
            picture[height, x + w - contour_strength] = color
        for width in range(x + contour_strength, x + w - contour_strength):
            picture[y + contour_strength, width] = color
            picture[y + h - contour_strength, width] = color


def draw_red_rectangle(x, y, w, h, picture, chunk_border):

    color = (1, 0, 0)

    for contour_strength in range(0, chunk_border):
        for height in range(y, y + h):
            picture[height, x + contour_strength] = color
            picture[height, x + w - contour_strength] = color
        for width in range(x + contour_strength, x + w - contour_strength):
            picture[y + contour_strength, width] = color
            picture[y + h - contour_strength, width] = color


def cropping(contours, img_PIL, filename, folder):
    """
    goes through all contours and creates a list of images
    :param contours: list with contours
    :param img_PIL: original image, called with PIL
    :param filename: filename of the image
    :param folder: foldername of the image
    :return: list with cropped and scaled images
    """

    cropped_list = list()   # list with cropped images

    # go through the list of contours
    for cnt in contours:
        x, y, w, h = cv2.boundingRect(cnt)     # get rectangle from contours
        cropped_image = img_PIL.crop((x, y, x+w, y+h))    # get rectangle from image
        
        # 0 ... 6492830432
        # raise Exception(x,y,w,h)
        # img_np = np.array(cropped_image)
        # raise Exception(str(cropped_image) +" " + str(x) +  " " + str (y) + " " +str(w)+ " " +str(h))
        img_ndarray = np.array(cropped_image)
        img_extended = create_extended_chunk(img_ndarray, filename, folder)
        img_extended_pil = Image.fromarray(img_extended)
        img_scaled = create_scaled_image(img_extended_pil, filename, folder) # scale image to 27x27 size HIER
        # 000000000

        cropped_list.append(img_scaled) # save in list

    return cropped_list


def create_extended_chunk(image_chunk, filename, folder):
    h, w = image_chunk.shape

    if h > w:
        extension_range = int((h - w) / 2)

        image_container = np.zeros((h, h))

        for w_in_container in range(extension_range, extension_range + w):
            for h_in_container in range(0, h):
                image_container[h_in_container, w_in_container] = \
                    image_chunk[h_in_container, w_in_container - extension_range]

        imsave(folder + filename + "_h_extened.png", image_container)
        return image_container

    elif w > h:
        extension_range = int((w - h) / 2)

        image_container = np.zeros((w, w))

        for w_in_container in range(0, w):
            for h_in_container in range(extension_range, extension_range + h):
                image_container[h_in_container, w_in_container] = \
                    image_chunk[h_in_container - extension_range, w_in_container]

        imsave(folder + filename + "_w_extened.png", image_container)
        return image_container

    else:
        imsave(folder + filename + "_q_extened.png", image_chunk)
        return image_chunk


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

    strl = list()
    strl.append(folder)
    strl.append(filename)
    strl.append('_centered.png')

    new_filename = ''.join(strl)

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


def clamp_float_values(img):
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
            else:
                img_np_array[y, x] = 0

    return img_np_array


def create_scaled_image(img_read, filename, folder):
    """
        Resize and change to aspect ratio of the image and save it to a given directory

        :parameter
            img_read: binary image array
            filename: name of the original image
            folder: directory of the new image

        :returns
            array of the scaled image
    """

    strl = list()
    strl.append(folder)
    strl.append(filename)
    strl.append('_scaled.png')

    new_filename = ''.join(strl)

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

    # img_np_clamp = clamp_binary_values(img_read)
    # img_pil_array = Image.fromarray(img_read)
    img_pil_array = img_read

    #new_filename = folder + "chunkScaled" + str(random.randrange(10)) + ".png"
    #imsave(new_filename, img_pil_array)
    # resize using Pillow
    img_cropped = img_pil_array.resize(image_dimension_t_small)
    img_ndarray = np.array(img_cropped)

    img_ndarray = clamp_float_values(img_ndarray)

    # img_cropped.save(new_filename)

    # reload image due to pillow using its own image class
    # return imread(newfilename)
    return img_ndarray


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


def get_image_rotation(filename, folder):
    """
        Get the Image Orientation Tag from an image and return it

        :parameter
            filename: name of the original image

        :returns
            EXIF file tag if it exists
    """

    file = open(folder + filename, 'rb')
    tags = exifread.process_file(file)

    for tag in tags.keys():
        if tag == 'Image Orientation':
            # print(f"{tag}, value {tags[tag]}")
            return tags[tag]


def get_image_rotation_from_location(directory):
    """
        Get the Image Orientation Tag from an image and return it

        :parameter
            filename: name of the original image

        :returns
            EXIF file tag if it exists
    """

    file = open(directory, 'rb')
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
        rotate_value = (str.split(str(rotation), " ")[1])
        if isinstance(rotate_value, int) or isinstance(rotate_value, float):
            value_cw = -float(rotate_value)
            img_rotated = rotate(img_read, value_cw)
            return img_rotated
        else:
            return img_read
    else:
        return img_read


def create_cropped_image(image, crop_border, filename, folder):

    image_cropped = image[crop_border:-crop_border, crop_border:-crop_border]

    return image_cropped


def read_images():
    """

        Creates a new folder for the process with the necessary sub folder.
        Starts the filtering process for each image.
        Read -> Resize -> Rotate -> Binary -> CenterOfMass -> Canny + Skeleton

    """

    path = abspath(__file__ + "/../../")
    data_path = str(path) + "/data/"
    json_path = str(path) + "/configs/settings.json"

    assign_json_values(json_path)

    main_folder = data_path + "filtered/" + datetime.datetime.now().strftime("%Y_%m_%d_x_%H_%M_%S")
    create_folder(main_folder)

    dir_name = data_path + "" + "image_green/"
    directory_data = listdir(dir_name)

    loaded_images = list()

    for file in directory_data:
        file_ends_with = file.split(".")[-1].lower()

        if len(loading_possible_filename) > 0:
            for filename in loading_possible_filename:
                if file_ends_with == filename:
                    loaded_images.append(file)
                else:
                    pass
                    # print("Could not find file with: " + filename + " at " + file)

    for image_name in loaded_images:
        # create folder and sub folder
        index = loaded_images.index(image_name)
        filename = f"{index}.jpg"

        sub_folder = main_folder + f"/{index}" + "/"
        create_folder(sub_folder)

        image_dir = dir_name + "/" + image_name

        # get rotation of image and read it
        rotation = get_image_rotation_from_location(image_dir)
        img_reading = imread(image_dir, plugin='matplotlib')

        # resize image
        img_scaled = create_scaled_image(img_as_ubyte(img_reading), filename, sub_folder)

        # rotate image
        img_rotated = rotate_image(img_scaled, rotation)

        # create binary image
        # img_binary = create_binary_image(img_rotated, filename, sub_folder)
        # img_binary = create_greenfiltered_image(img_rotated, filename, sub_folder)
        img_binary = create_chromakey_image(img_rotated, filename, sub_folder)

        # get black borders inside of image
        img_borders = create_borders(img_binary, filename, sub_folder)

        # create two filtered images
        img_canny = create_canny_image(img_borders, filename, sub_folder)   # UNUSED!
        img_skeleton = create_skeleton_image(img_borders, filename, sub_folder)

        # align binary image to center of mass
        img_com = create_com_image(img_skeleton, filename, sub_folder)

    # ###############################CODE BACKUP##############################################
    # for i in range(0, 4):
    #     filename = f"{i}.jpg"
    #     dir_name = data_path + "" + "image_green/" + filename

        # create folder and sub folder
        # sub_folder = main_folder + f"/{i}" + "/"
        # create_folder(sub_folder)

        # get rotation of image and read it
        # rotation = get_image_rotation(dir_name)
        # img_reading = imread(dir_name, plugin='matplotlib')

        # resize image
        # img_scaled = create_scaled_image(img_as_ubyte(img_reading), filename, sub_folder)

        # rotate image
        # img_rotated = rotate_image(img_scaled, rotation)

        # create binary image
        # img_binary = create_binary_image(img_rotated, filename, sub_folder)
        # img_binary = create_greenfiltered_image(img_rotated, filename, sub_folder)
        # img_binary = create_chromakey_image(img_rotated, filename, sub_folder)

        # get black borders inside of image
        # img_borders = borders(img_binary, filename, sub_folder)

        # create two filtered images
        # img_canny = create_canny_image(img_borders, filename, sub_folder)   # UNUSED!
        # img_skeleton = create_skeleton_image(img_borders, filename, sub_folder)

        # align binary image to center of mass
        # img_com = create_com_image(img_skeleton, filename, sub_folder)


def read_image_from_location(directory):

    path = abspath(__file__ + "/../../")
    json_path = str(path) + "/configs/settings.json"

    # get new json values and assign them
    assign_json_values(json_path)

    data_path = path + "/filtered/"
    filename = "filtered.png"

    main_folder = data_path                                                                     # + "/ImageFilter" + "/"
    create_folder(main_folder)

    # get rotation of image and read it
    rotation = get_image_rotation_from_location(directory)
    img_reading = imread(directory, plugin='matplotlib')

    # resize image
    img_scaled = create_scaled_image(img_as_ubyte(img_reading), filename, main_folder)

    # rotate image
    img_rotated = rotate_image(img_scaled, rotation)

    # create binary image
    img_binary = create_chromakey_image(img_rotated, filename, main_folder)

    # get black borders inside of image
    img_borders = create_borders(img_binary, filename, main_folder)

    # create filtered images
    img_skeleton = create_skeleton_image(img_borders, filename, main_folder)

    # align binary image to center of mass
    img_com = create_com_image(img_skeleton, filename, main_folder)

    return img_com


def read_images_with_chunks():
    """

        Creates a new folder for the process with the necessary sub folder.
        Starts the filtering process for each image.
        Read -> Resize -> Rotate -> Binary -> CenterOfMass -> Canny + Skeleton

    """

    # TODO: add to settings.json
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

        img_np_pre_cropped = create_cropped_image(img_rotated,
                                                  pre_border,
                                                  filename,
                                                  main_folder)

        # create binary image
        img_binary = create_chromakey_image(img_np_pre_cropped, filename, main_folder)

        # Returned lists by chunking
        list_of_work_images, list_of_work_contours, img_with_chunks = create_chunked_image(img_binary, filename,
                                                                                              main_folder, img_reading)

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

                #schmiering
                img_fillout = create_fillout_image(img_clamp, chunk_filename, main_folder)

                # get black borders inside of image
                img_borders = create_borders(img_fillout, chunk_filename, main_folder)

                # create filtered images
                img_skeleton = create_skeleton_image(img_borders, chunk_filename, main_folder)

                # align binary image to center of mass
                img_com = create_com_image(img_skeleton, chunk_filename, main_folder)

                list_of_return_images.append(img_com)
                list_of_return_contours.append(index_coord)

    return list_of_return_images, list_of_return_contours, img_with_chunks


def read_image_with_chunks_from_location(directory):

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

    img_pre_crop = create_cropped_image(img_rotated,pre_border,filename,main_folder)

    # create binary image
    img_binary = create_chromakey_image(img_pre_crop, filename, main_folder)

    # TODO: Add chunking here with image reading from directory
    # Returned lists by chunking
    list_of_work_images, list_of_work_contours, img_with_chunks = create_chunked_image(img_binary, filename, main_folder, img_reading)

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

            img_fillout = create_fillout_image(img_clamp, chunk_filename, main_folder)
            # TODO REDUCED

            # get black borders inside of image
            img_borders = create_borders(img_fillout, chunk_filename, main_folder)

            # create filtered images
            img_skeleton = create_skeleton_image(img_borders, chunk_filename, main_folder)

            # align binary image to center of mass
            img_com = create_com_image(img_skeleton, chunk_filename, main_folder)

            list_of_return_images.append(img_com)
            list_of_return_contours.append(index_coord)

        return list_of_return_images, list_of_return_contours, img_with_chunks


def main():

    read_images_with_chunks()


if __name__ == "__main__":
    t1 = time.time()

    main()

    t2 = time.time()

    # print("Passed time: " + str(t2 - t1))
