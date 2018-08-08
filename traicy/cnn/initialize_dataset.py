import glob
import pickle
from os.path import abspath
from random import shuffle
from skimage.io import imread
from skimage.util import img_as_float
import numpy as np
import tensorflow as tf

buchstaben = ["A", "B"]#, "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z"]
file_list = [] #bilddateien
labels_list = []

sublist_train = []
sublist_eval = []
sublist_test = []


def generator_train():
    for index in range(0, len(sublist_train)):
        image = imread(sublist_train[index][0], as_grey=True)
        image_flat = image.flatten()
        image_float = img_as_float(image_flat)
        label = sublist_train[index][1]
        yield image_float, label


def generator_eval():
    for index in range(0, len(sublist_eval)):
        image = imread(sublist_eval[index][0], as_grey=True)
        image_flat = image.flatten()
        image_float = img_as_float(image_flat)
        label = sublist_eval[index][1]
        yield image_float, label


def generator_test():
    for index in range(0, len(sublist_test)):
        image = imread(sublist_test[index][0], as_grey=True)
        image_flat = image.flatten()
        image_float = img_as_float(image_flat)
        label = sublist_test[index][1]
        yield image_float, label


def load_all_data():
    #gives back lists
    ####SET PATHS####
    path = abspath(__file__ + "/../../")  # change directory to traicy
    traicy_data_path = path + "/cnn/TRAICY_data/"  # save in folder

    ####GET ALL FILES IN A LIST####
    for dir in buchstaben:
        directory = traicy_data_path + dir + "/"
        for filename in glob.glob(directory + '*.png'):  # only jpg
            file_list.append(filename)
            labels_list.append(dir)

    both_lists = np.column_stack((file_list,labels_list))

    np.random.shuffle(both_lists)

    return both_lists


def get_sublist(list_complete, size_train, size_eval, size_test):
    list = list_complete
    sublist_train = []
    sublist_eval = []
    sublist_test = []
    s_index = 0

    for let in buchstaben: #für jeden buchstaben
        for count in range(size_train): #jeder buchstabe wird x mal gebraucht
            index = 0
            found = False
            while (found is not True):
                if(list[index,1] == let):
                    #sublist[s_index, 0] = list[index, 0]
                    #sublist[s_index, 1] = list[index, 1]
                    sublist_train.append((list[index, 0], list[index, 1]))
                    np.delete(list, index)
                    found = True
                else: index += 1

    for let in buchstaben: #für jeden buchstaben
        for count in range(size_eval): #jeder buchstabe wird x mal gebraucht
            index = 0
            found = False
            while (found is not True):
                if(list[index,1] == let):
                    #sublist[s_index, 0] = list[index, 0]
                    #sublist[s_index, 1] = list[index, 1]
                    sublist_eval.append((list[index, 0], list[index, 1]))
                    np.delete(list, index)
                    found = True
                else: index += 1

    for let in buchstaben: #für jeden buchstaben
        for count in range(size_test): #jeder buchstabe wird x mal gebraucht
            index = 0
            found = False
            while (found is not True):
                if(list[index,1] == let):
                    #sublist[s_index, 0] = list[index, 0]
                    #sublist[s_index, 1] = list[index, 1]
                    sublist_test.append((list[index, 0], list[index, 1]))
                    np.delete(list, index)
                    found = True
                else: index += 1

    np.random.shuffle(sublist_train)
    np.random.shuffle(sublist_eval)
    np.random.shuffle(sublist_test)

    return np.asarray(sublist_train), np.asarray(sublist_eval), np.asarray(sublist_test)


def set_all_datasets():
    train = tf.data.Dataset.from_generator(generator=generator_train, output_types=(tf.float32, tf.string))
    eval = tf.data.Dataset.from_generator(generator=generator_eval, output_types=(tf.float32, tf.string))
    test = tf.data.Dataset.from_generator(generator=generator_test, output_types=(tf.float32, tf.string))
    # train = tf.data.Dataset.from_tensor_slices(sublist_train)
    # eval = tf.data.Dataset.from_tensor_slices(sublist_eval)
    # test = tf.data.Dataset.from_tensor_slices(sublist_test)

    return train, eval, test


class TraicyData:

    train = None
    eval = None
    test = None

    def __init__(self, train=None, eval=None, test=None):
        if train is not None:
            self.train = train
        if eval is not None:
            self.eval = eval
        if test is not None:
            self.test = test


def parse_data():
    global sublist_train, sublist_eval, sublist_test

    lists = load_all_data()
    sublist_train, sublist_eval, sublist_test = get_sublist(lists, 30, 30, 30)  # 1923, 385, 140
                                                                                # 49.998 Trainingsdaten,
                                                                                # 10010 Evaluierungsdaten,
                                                                                # 3640 Testdaten
    train, test, eval = set_all_datasets() # funktioniert das??
    td = TraicyData(train, test, eval)

    return td


traicy = parse_data()
iterator = traicy.test.make_one_shot_iterator()
iterValue = iterator.get_next()

sess = tf.Session()
print(sess.run(iterValue))
