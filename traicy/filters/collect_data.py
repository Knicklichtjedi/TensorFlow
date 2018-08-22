from os import listdir
from os.path import abspath
import glob

import cv2
from PIL import Image
from skimage import filters as filters, img_as_uint, img_as_ubyte, img_as_float
from skimage.color import rgb2gray, gray2rgb
from skimage.io import imread, imsave
import ImageFilter_noLoad

file_list = []
labels_list = []

data_path_raw = ""
traicy_data_path = ""

buchstaben = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z"]


def get_labels_and_data():
    ####SET PATHS####
    path = abspath(__file__ + "/../../")  # change directory to traicy
    traicy_data_path = path + "/cnn/TRAICY_data/"  # save in folder

    ####GET ALL FILES IN A LIST####
    for dir in buchstaben:
        directory = data_path_raw + dir + "/"
        for filename in glob.glob(directory + '*.jpg'):  # only jpg
            file_list.append(filename)
            labels_list.append(dir)
    return file_list, labels_list


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
    # img_threshold = filters.threshold_mean(img_conv_float)
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


def get_cropped_image(contour, image, label, index, indexSheet):
    x, y, w, h = cv2.boundingRect(contour)
    cropped_image = image.crop((x, y, x + w, y + h))

    imsave(traicy_data_path +  label + "/" + str(indexSheet) + str(index) + ".jpg", img_as_uint(cropped_image))
    #print(traicy_data_path +  label + "/" + str(indexSheet) + str(index) + ".jpg")

    return cropped_image


def main():
    #set paths & create the file lists
    file_list, labels_list = set_lists()

    #go through all files
    if (file_list.__len__() == labels_list.__len__()):
        for index in range(90, 96): #len(file_list)  #A: 0-6 B: 6-12 C: 12-18 D: 18-24 E: 24-30 F: 30-36 G: 36-42 H: 42-48 I: 48-54 (Konturlänge 5) J: 54-60 K: 60-66 L: 66-72 M: 72-78 N: 78-84 O: 84-90 P: 90-96 !!! Q 96-102 R: 102-108 S: 108-114 T: 114-120, U: 120-126 V: 126-132 W: 132-138 X: 138-144 Y: 144-150 Z: 150-156
            label = labels_list[index]
            binary_file = toBinary(file_list[index])
            border_file = borders(binary_file, file_list[index])
            contours = get_contours(border_file, file_list[index])
            rgb_border_file = gray2rgb(border_file)


            cropped_images = []
            for cnt in contours:
                x, y, w, h = cv2.boundingRect(cnt)
                ImageFilter_noLoad.draw_red_rectangle(x, y, w, h, rgb_border_file, 1)

                crop = get_cropped_image(cnt, Image.open(file_list[index]), label, indexCrops, index)
                cropped_images.append(crop)

            imsave(data_path_raw +"binary/"+ "borders_" + label + str(index) + "_K_" + str(len(contours)) + ".png", img_as_uint(rgb_border_file))

    #with open(traicy_data_path + "labels.txt", 'w') as the_file:
    #    the_file.write(all_labels)


if __name__ == "__main__":
    main()