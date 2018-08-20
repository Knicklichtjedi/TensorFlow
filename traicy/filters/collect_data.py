from os import listdir
from os.path import abspath
import glob

import cv2
from PIL import Image
from skimage import filters as filters, img_as_uint, img_as_ubyte, img_as_float
from skimage.color import rgb2gray, gray2rgb
from skimage.io import imread, imsave
import image_filter

# list of files /pathnames
file_list = []
# list of labels corresponding to the image file_list
labels_list = []

# path to raw data (read path)
data_path_raw = ""
# path to new data (save path)
traicy_data_path = ""

# array with letters that define the directories to read from and the labels of the imagedata
letters = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V",
           "W", "X", "Y", "Z"]

# minimal contour length of a crop
contour_size = 100

# threshold for binary image
img_threshold = 0.8


# reads the raw data and gives them back in two lists for image paths and labels
def get_labels_and_data():

    # get all files and labels in a list
    for dir in letters:  # for every directory
        directory = data_path_raw + dir + "/"  # set directory path
        for filename in glob.glob(directory + '*.jpg'):  # every jpg file paths
            file_list.append(filename)  # append path
            labels_list.append(dir)  # append label / directory name
    return file_list, labels_list


# get binary coloured file
def to_binary(file):
    img_conv = rgb2gray(imread(file, plugin='matplotlib')) # convert to gray

    img_conv_float = img_as_float(img_conv)  # get float image

    img_gaussian = filters.gaussian(img_conv_float, 0.5) # set gaussian filter
    img_binary = img_gaussian < img_threshold # get binary

    imsave(file + "binary.png", img_as_uint(img_binary)) # save image

    return img_binary


# create borders on an image
def borders(img, filename):
    new_color = 0 # color of border
    image_border = 10 # size of border
    xrange, yrange = img.shape # get range of image

    for x in range(0, xrange): # iterate through image at the border
        for y in range(0, image_border):
            img[x, y] = new_color # set color in y-direction on top

        for y in range(yrange - image_border, yrange):
            img[x, y] = new_color # set color in y-direction at bottom

    for y in range(0, yrange): # iterate through image
        for x in range(0, image_border):
            img[x, y] = new_color # set color in x-direction on top

        for x in range(xrange - image_border, xrange):
            img[x, y] = new_color # set color in y-direction at bottom

    # sve image
    imsave(filename + "borders.png", img_as_uint(img))

    return img


# gets contours of an binary image and returns an array of the best contours
def get_contours(img, filename):
    thresh = img_as_ubyte(img) # threshold
    im2, contours, hierarchy = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE) # find contours. RETR_EXTERNAL = only gets external contours, CHAIN_APPROX_SIMPLE = gives a list, not a tree

    best_contours = []  # save contours in a list
    for cnt in contours: # for every contour
        if cv2.contourArea(cnt) > contour_size: # if contour is long enough
            best_contours.append(cnt) # append to list

    imsave(filename + "borders.png", img_as_uint(img)) # save file

    return best_contours


# this method gets a contour and an image and cuts out the contour from the original image to save the new crop and give it back
def get_cropped_image(contour, image, label, index, indexSheet):
    x, y, w, h = cv2.boundingRect(contour)  # get coordinates of contours
    cropped_image = image.crop((x, y, x + w, y + h))  # crop image

    # save crop
    imsave(traicy_data_path + label + "/" + str(indexSheet) + str(index) + ".jpg", img_as_uint(cropped_image))

    return cropped_image


# main method that is called to extract crops 
def main():
    # set paths & create the file lists
    file_list, labels_list = get_labels_and_data()

    # go through all files
    if (len(file_list) == len(labels_list)):  # if the lists have the same length
        for index in range(len(labels_list)):  # go through list
            label = labels_list[index]  # get label
            binary_file = to_binary(file_list[index])  # get binary coloured image file
            border_file = borders(binary_file, file_list[index])  # apply borders to image
            contours = get_contours(border_file, file_list[index])  # get contours of letters
            rgb_border_file = gray2rgb(border_file)  # get grey file

            # index for counting the crops (naming the files)
            index_crops = 0
            # array that contains cropped images
            cropped_images = []
            for cnt in contours:  # for every contours
                x, y, w, h = cv2.boundingRect(cnt)  # get rectangle
                image_filter.draw_red_rectangle(x, y, w, h, rgb_border_file, 1)  # draw rectangle
                crop = get_cropped_image(cnt, Image.open(file_list[index]), label, index_crops, index)  # get crop
                cropped_images.append(crop)  # append to list


# calls main method
if __name__ == "__main__":
    main()
