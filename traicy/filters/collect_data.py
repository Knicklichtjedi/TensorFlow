from os import listdir
from os.path import abspath
import glob

import cv2
from PIL import Image
from skimage import filters as filters, img_as_uint, img_as_ubyte, img_as_float
from skimage.color import rgb2gray, gray2rgb
from skimage.io import imread, imsave

import image_filter as filter

# list of files /pathnames
from image_filters.contours import draw_red_rectangle

file_list = []
# list of labels corresponding to the image file_list
labels_list = []

# absolute path to parent directory traicy
file_path = abspath("./../")

# path to raw data (read path)
data_path_raw = file_path + "/data/data_RAW/"
# path to new data (save path)
traicy_data_path = file_path + "/cnn/TRAICY_data/"

# array with letters that define the directories to read from and the labels of the imagedata
letters = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V",
           "W", "X", "Y", "Z"]

# minimal contour length of a crop
contour_size = 80

# threshold for binary image
img_threshold = 0.8


def get_labels_and_data():
    """
    reads the raw data and gives them back in two lists for image paths and labels
    :return: file_list with image filenames and labels_list with labels
    """

    # get all files and labels in a list
    for directory in letters:  # for every directory
        directory_label = directory
        directory = data_path_raw + directory + "/"  # set directory path
        for filename in glob.glob(directory + '*.jpg'):  # every jpg file paths
            file_list.append(filename)  # append path
            labels_list.append(directory_label)  # append label / directory name
        print(directory)
    return file_list, labels_list


def to_binary(file):
    """
    get binary coloured file
    :param file: image file
    :return: binary image
    """
    img_conv = rgb2gray(imread(file, plugin='matplotlib'))  # convert to gray

    img_conv_float = img_as_float(img_conv)  # get float image

    img_gaussian = filters.gaussian(img_conv_float, 0.5)
    img_binary = img_gaussian < img_threshold

    imsave(file + "binary.png", img_as_uint(img_binary))  # save image

    return img_binary


#
def borders(img, filename):
    """
    create borders on an image
    :param img: image
    :param filename: filepath
    :return: image with borders
    """
    new_color = 0  # color of border
    image_border = 10  # size of border
    xrange, yrange = img.shape  # get range of image

    for x in range(0, xrange):  # iterate through image at the border
        for y in range(0, image_border):
            img[x, y] = new_color  # set color in y-direction on top

        for y in range(yrange - image_border, yrange):
            img[x, y] = new_color  # set color in y-direction at bottom

    for y in range(0, yrange):  # iterate through image
        for x in range(0, image_border):
            img[x, y] = new_color  # set color in x-direction on top

        for x in range(xrange - image_border, xrange):
            img[x, y] = new_color  # set color in y-direction at bottom

    # sve image
    imsave(filename + "borders.png", img_as_uint(img))

    return img


def get_contours(img, filename):
    """
    gets contours of an binary image and returns an array of the best contours
    :param img: image
    :param filename: filepath
    :return: list of best contours
    """
    thresh = img_as_ubyte(img)  # threshold
    im2, contours, hierarchy = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)  # find contours.
    # RETR_EXTERNAL = only gets external contours, CHAIN_APPROX_SIMPLE = gives a list, not a tree

    best_contours = []  # save contours in a list
    for cnt in contours:  # for every contour
        if cv2.contourArea(cnt) > contour_size:  # if contour is long enough
            best_contours.append(cnt)  # append to list

    imsave(filename + "borders.png", img_as_uint(img))  # save file

    return best_contours


def get_cropped_image(contour, image, label, index, index_sheet):
    """
    this method gets a contour and an image and cuts out the contour from the original image to save the new crop
    and give it back
    :param contour: contour with x,y,w,h of a rectangle
    :param image: image to take crop from
    :param label: label of the crop
    :param index: index of the crop
    :param index_sheet: index of the sheet where the crop came from
    :return: cropped image
    """
    x, y, w, h = cv2.boundingRect(contour)  # get coordinates of contours
    cropped_image = image.crop((x, y, x + w, y + h))  # crop image

    filter.create_folder(traicy_data_path + label + "/")

    # save crop
    imsave(traicy_data_path + label + "/" + str(index_sheet) + str(index) + ".jpg", img_as_uint(cropped_image))

    return cropped_image


def main():
    """
    main method that is called to extract crops
    """
    # set paths & create the file lists
    file_list_main, labels_list_main = get_labels_and_data()

    # go through all files
    if len(file_list_main) == len(labels_list_main):  # if the lists have the same length
        for index in range(len(labels_list_main)):  # go through list
            label = labels_list_main[index]  # get label
            binary_file = to_binary(file_list_main[index])  # get binary coloured image file
            border_file = borders(binary_file, file_list_main[index])  # apply borders to image
            contours = get_contours(border_file, file_list_main[index])  # get contours of letters
            rgb_border_file = img_as_float(gray2rgb(border_file))  # get grey file

            # index for counting the crops (naming the files)
            index_crops = 0
            # array that contains cropped images
            cropped_images = []
            for cnt in contours:  # for every contours
                x, y, w, h = cv2.boundingRect(cnt)  # get rectangle
                draw_red_rectangle(x, y, w, h, rgb_border_file, 1)  # draw rectangle
                crop = get_cropped_image(cnt, Image.open(file_list_main[index]), label, index_crops, index)  # get crop
                cropped_images.append(crop)  # append to list
                index_crops += 1

            imsave(file_list_main[index] + "contours.png", img_as_uint(rgb_border_file))


# calls main method
if __name__ == "__main__":
    main()
