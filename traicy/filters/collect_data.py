from os import listdir
from os.path import abspath
import glob

import cv2
from PIL import Image
from skimage.io import imread, imsave
from skimage.color import rgb2gray
from skimage import filters as filters, img_as_uint, img_as_ubyte, img_as_float

import ImageFilter_noLoad as im_filter

file_list = []
labels_list = []

data_path_raw = ""
traicy_data_path = ""


def set_lists():
    ####SET PATHS####
    path = abspath(__file__ + "/../../")  # change directory to traicy
    global data_path_raw
    global traicy_data_path
    data_path_raw= path + "/data/data_RAW/"  # read from folder
    traicy_data_path = path + "/cnn/TRAICY_data/"  # save in folder

    ####GET ALL FILES IN A LIST####
    for filename in glob.glob(data_path_raw + '*.jpg'):  # only png
        file_list.append(filename)

    ####GET ALL LABEL FILES IN A LIST####
    for label_filename in glob.glob(data_path_raw + '*.txt'):  # only png
        label_file = open(label_filename, "r")
        label_text = label_file.read()
        labels_list.append(label_text)

    return file_list, labels_list


def toBinary(file):
    img_conv = rgb2gray(imread(file, plugin='matplotlib'))

    img_conv_float = img_as_float(img_conv)

    img_gaussian = filters.gaussian(img_conv_float, 0.5)
    #img_threshold = filters.threshold_mean(img_conv_float)
    img_threshold = 0.8
    img_binary = img_gaussian < img_threshold

    imsave(file + "binary.png", img_as_uint(img_binary))

    return img_binary


def borders(img, filename):

    new_color = 0
    image_border = 10
    xrange, yrange = img.shape

    for x in range(0, xrange):
        for y in range(0, image_border):
            img[x, y] = new_color

        for y in range(yrange - image_border, yrange):
            img[x, y] = new_color

    for y in range(0, yrange):
        for x in range(0, image_border):
            img[x, y] = new_color

        for x in range(xrange - image_border, xrange):
            img[x, y] = new_color

    imsave(filename + "borders.png", img_as_uint(img))

    return img


def get_contours(img, filename):
    thresh = img_as_ubyte(img)
    im2, contours, hierarchy = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    image_with_chunks = Image.open(filename)

    count = 0
    best_contours = []  # save contours in a list
    for cnt in contours:
        if cv2.contourArea(cnt) > 100:
            best_contours.append(cnt)

    print("Anzahl der gefundenen Konturen:" + str(best_contours.__len__()))

    imsave(filename + "borders.png", img_as_uint(img))

    return best_contours


def get_cropped_image(contour, image):
    x, y, w, h = cv2.boundingRect(contour)
    cropped_image = image.crop((x, y, x + w, y + h))

    imsave(traicy_data_path + str(x) + str(y) + str(w) + str(h) + "crop.png", img_as_uint(cropped_image))

    return cropped_image


def main():
    #set paths & create the file lists
    file_list, labels_list = set_lists()

    #go through all files
    if (file_list.__len__() == labels_list.__len__()):
        for index in range(0, file_list.__len__()):
            binary_file = toBinary(file_list[index])
            border_file = borders(binary_file, file_list[index])
            contours = get_contours(border_file, file_list[index])

            cropped_images = []
            for cnt in contours:
                crop = get_cropped_image(cnt, Image.open(file_list[index]))
                cropped_images.append(crop)

            print("Anzahl der crops:" + str(cropped_images.__len__()))
            print(labels_list[index])


 # get labels (csv textfile) for specific original image file and write an array: labels_arr
# get image, use threshold function to create binary image
# get letters with contours function and save the location in an array: contours_arr
# go through labels_arr with index
# take contours at index and save image from contours coordinates
# take a time stamp as name and save it at a specific location for your training data, in a folder with the name of the label


if __name__ == "__main__":
    main()