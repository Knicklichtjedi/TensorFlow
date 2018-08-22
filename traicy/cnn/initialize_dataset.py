import glob
import pickle
from pathlib import Path
from skimage.io import imread
from skimage.util import img_as_float
import numpy as np


# The TraicyData class saves the data in several arrays, so that the neural network can access them easily
# train_img: images of the training data
# eval_img: images of the eval_data
# test_img: images of the test_data
# train_label: labels corresponding to the images of the train_data
# eval_label: labels corresponding to the images of the eval_data
# test_label: labels corresponding to the images of the test_data
class TraicyData:
    train_img = None
    eval_img = None
    test_img = None
    train_label = None
    eval_label = None
    test_label = None

    def __init__(self, train_img=None, eval_img=None, test_img=None, train_label=None, eval_label=None,
                 test_label=None):
        if train_img is not None:
            self.train_img = train_img
        if eval_img is not None:
            self.eval_img = eval_img
        if test_img is not None:
            self.test_img = test_img
        if train_label is not None:
            self.train_label = train_label
        if eval_label is not None:
            self.eval_label = eval_label
        if test_label is not None:
            self.test_label = test_label


# letters array that contains all the letters that the dataset should use
# ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W",
#  "X", "Y", "Z"]
letters = ["T", "R", "A", "I", "C", "Y"]

# directory TRAICY_data
traicy_data_path = "TRAICY_data/"
# localization and name of the serialized file
filename = "trai.cy"

# train data to train the NN
sublist_train = []
# evaluation data for the NN to find the error rate
sublist_eval = []
# test data for the user to check how the NN performs on unseen content with the same origin
sublist_test = []

# size of sublist_train
train_size = 2236
# size of sublist_eval
eval_size = 208
# size of sublist_test
test_size = 4


def get_serialized_file():
    """
    gets arrays of trainings, test and evaluation data for images and labels, saves them in an TraicyData instance
    and writes it to a binary file
    :return: True if file was written, False if not
    """
    train_img, eval_img, test_img, train_label, eval_label, test_label = parse_data_as_array()  # get arrays
    td = TraicyData(train_img, eval_img, test_img, train_label, eval_label, test_label)  # save into object
    write_datafile(filename, td)  # write binary file

    # check if file was created
    file = Path(filename)
    try:
        file.resolve()
    except FileNotFoundError:
        return False
    else:
        return True


def parse_data_as_array():
    """
    loads all TRAICY_data and changes them into useful images and labels arrays for training, testing and evaluation
    and gives them back
    :return: six arrays of training-, test- and evaluation images and labels
    """
    global sublist_train, sublist_eval, sublist_test  # get global variables

    lists = load_all_data()  # load all data rom TRAICY_data directory

    sublist_train, sublist_eval, sublist_test = get_sublist(lists, train_size, eval_size,
                                                            test_size)  # change to sublists

    # get arrays from generators for images and labels lists only
    train_img = np.asarray(list(generator_train_img()), dtype=np.float32)
    eval_img = np.asarray(list(generator_eval_img()), dtype=np.float32)
    test_img = np.asarray(list(generator_test_img()), dtype=np.float32)
    train_label = np.asarray(list(generator_train_label()), dtype=np.int32)
    eval_label = np.asarray(list(generator_eval_label()), dtype=np.int32)
    test_label = np.asarray(list(generator_test_label()), dtype=np.int32)

    return train_img, eval_img, test_img, train_label, eval_label, test_label


def load_all_data():
    """
    read all data from the traicy_data_path directory according to the directories that have the names of the labels
    defined in the letters array
    :return: list of images and labels
    """

    # initialize array for both images and labels list
    images_and_labels_list = []

    # index to change the letters into numbers and save them as labes (e.g. A=0, B=1, etc.)
    label_index = 0
    for directory in letters:  # for every directory in TRAICY_data
        list_file = list()  # set file and labels lists
        list_label = list()
        directory = traicy_data_path + directory + "/"  # get directory of the letter

        for file in glob.glob(directory + '*.png'):  # for every file in the letter directory
            list_file.append(file)  # append file and label to the corresponding list
            list_label.append(label_index)

        im_and_labels_of_letter_list = np.column_stack((list_file, list_label))  # both images and labels in one list
        np.random.shuffle(im_and_labels_of_letter_list)  # shuffle the array
        size = len(im_and_labels_of_letter_list)  # get size, needed at for-loop

        for indexlist in range(0, size):  # for every tupel in the im_and_labels_of_letter_list
            # append the tupel to the images_and_labels_lists that has all letters
            images_and_labels_list.append(
                (im_and_labels_of_letter_list[indexlist, 0], im_and_labels_of_letter_list[indexlist, 1]))

        label_index += 1  # increment the index for the next letter

    return images_and_labels_list


def generator_train_img():
    """
    generator for the Dataset of the train_img array
    :return: train_img
    """
    for index in range(0, len(sublist_train)):
        image = imread(sublist_train[index][0], as_grey=True)
        image_flat = image.flatten()
        image_float = img_as_float(image_flat)
        yield image_float


def generator_train_label():
    """
    generator for the Dataset of the train_label array
    :return: train_label
    """
    for index in range(0, len(sublist_train)):
        label = int(sublist_train[index][1])
        yield label


def generator_eval_img():
    """
    generator for the Dataset of the eval_label array
    :return: eval_img
    """
    for index in range(0, len(sublist_eval)):
        image = imread(sublist_eval[index][0], as_grey=True)
        image_flat = image.flatten()
        image_float = img_as_float(image_flat)
        yield image_float


def generator_eval_label():
    """
    generator for the Dataset of the eval_label array
    :return: eval_label
    """
    for index in range(0, len(sublist_eval)):
        label = int(sublist_eval[index][1])
        yield label


def generator_test_img():
    """
    generator for the Dataset of the test_img array
    :return: test_img
    """
    for index in range(0, len(sublist_test)):
        image = imread(sublist_test[index][0], as_grey=True)
        image_flat = image.flatten()
        image_float = img_as_float(image_flat)
        yield image_float


def generator_test_label():
    """
    generator for the Dataset of the test_label array
    :return: test_label
    """
    for index in range(0, len(sublist_test)):
        label = int(sublist_test[index][1])
        yield label


def get_sublist(list_complete, size_train, size_eval, size_test):
    """
    this method is used to change extract three sublists of one list.
    :param list_complete: full list
    :param size_train: number of images per label to be inserted into training data
    :param size_eval: number of images per label to be inserted into eval data
    :param size_test: number of images per label to be inserted into test data
    :return: three sublists of former list
    """
    main_list = list_complete
    # create sublists
    sublist_train = []
    sublist_eval = []
    sublist_test = []
    sublist = []
    size = 0

    for lists in range(3):  # go through all sublists

        sublist.clear()  # clear list

        # set size
        if lists == 0:
            size = train_size
        elif lists == 1:
            size = eval_size
        elif lists == 2:
            size = test_size
        else:
            size = 0

        print(size)

        # index for the letter labels
        index_letter = 0
        for let in letters:  # for every letter
            for count in range(int(size)):  # for every picture/label you want to insert

                # final index. helps to not go through parts of the lists that has already been visited
                index = 0
                # boolean that says whether the correct letter was found or not
                found = False
                while found is not True and index < len(
                        main_list):  # while the correct letter wasnt found and below the length of the list
                    if int(main_list[index][1]) == index_letter:  # if you found the correct label
                        sublist.append((main_list[index][0], main_list[index][1]))  # add to sublist
                        np.delete(main_list, index)  # delete from main_list to avoid duplicate
                        found = True  # set found true ... repeat cylce
                    else:  # if label is incorrect

                        index += 1  # next row in the main_list
            index_letter += 1  # new letter

        # set sublists
        if lists == 0:
            sublist_train = sublist
        elif lists == 1:
            sublist_eval = sublist
        elif lists == 2:
            sublist_test = sublist

    return np.asarray(sublist_train), np.asarray(sublist_eval), np.asarray(sublist_test)


def write_datafile(filename_obj, obj):
    """
    writes a serilized file from an object using pickle
    :param filename_obj: filepath
    :param obj: object that should be written
    """
    with open(filename_obj, 'wb') as f:
        pickle.dump(obj, f)


def read_datafile(filename_obj):
    """
    reads a datafile using pickle and converts it to a TraicyData object.
    :param filename_obj: filepath
    :return: TracyData object with arrays of labels and image for training, test and evaltuation purposes
    """
    with open(filename_obj, 'rb') as f:
        var = pickle.load(f)

        traicy = TraicyData(var.train_img, var.eval_img, var.test_img, var.train_label, var.eval_label, var.test_label)

        return traicy


def main():
    """
    this method is only called to debug the script. it creates and reads a dataset. it should NOT be called from
    another script.
    """
    global traicy_data_path, filename  # global statement gets variables from outer scope

    traicy_data_path = "TRAICY_data/"  # set path to TRAICY_data
    filename = "trai.cy"  # set the name of your serialized file

    get_serialized_file()  # read the TRAICY_data Dataset and serialize a TraicyData class to the file
    traicy_data_loaded = read_datafile(filename)  # read and deserialize the file

    # print the labels of the three arrays you created to check if they are correct
    print(traicy_data_loaded.train_label, traicy_data_loaded.eval_label, traicy_data_loaded.test_label)


# calls the main method for debugging
if __name__ == "__main__":
    main()
