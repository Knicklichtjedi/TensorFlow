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


def generator_train_img():
    for index in range(0, len(sublist_train)):
        image = imread(sublist_train[index][0], as_grey=True)
        image_flat = image.flatten()
        image_float = img_as_float(image_flat)
        yield image_float


def generator_train_label():
    for index in range(0, len(sublist_train)):
        label = int(sublist_train[index][1])
        yield label


def generator_eval_img():
    for index in range(0, len(sublist_eval)):
        image = imread(sublist_eval[index][0], as_grey=True)
        image_flat = image.flatten()
        image_float = img_as_float(image_flat)
        yield image_float


def generator_eval_label():
    for index in range(0, len(sublist_eval)):
        label = int(sublist_eval[index][1])
        yield label


def generator_test_img():
    for index in range(0, len(sublist_test)):
        image = imread(sublist_test[index][0], as_grey=True)
        image_flat = image.flatten()
        image_float = img_as_float(image_flat)
        yield image_float


def generator_test_label():
    for index in range(0, len(sublist_test)):
        label = int(sublist_test[index][1])
        yield label

def load_all_data():
    #gives back lists
    ####SET PATHS####
    path = abspath(__file__ + "/../../")  # change directory to traicy
    traicy_data_path = path + "/cnn/TRAICY_data/"  # save in folder

    ####GET ALL FILES IN A LIST####
    index = 0
    for dir in buchstaben:
        directory = traicy_data_path + dir + "/"
        for filename in glob.glob(directory + '*.png'):  # only jpg
            file_list.append(filename)
            labels_list.append(index)
        index+=1

    both_lists = np.column_stack((file_list,labels_list))

    np.random.shuffle(both_lists)

    return both_lists


def get_sublist(list_complete, size_train, size_eval, size_test):
    list = list_complete
    sublist_train = []
    sublist_eval = []
    sublist_test = []
    s_index = 0

    print(str(len(list)))

    indexBuch = 0
    for let in buchstaben: #für jeden buchstaben
        for count in range(size_train): #jeder buchstabe wird x mal gebraucht
            index = 0
            found = False
            while (found is not True and index < len(list)):
                a = list[index,1]
                if(int(list[index,1]) == indexBuch):
                    #sublist[s_index, 0] = list[index, 0]
                    #sublist[s_index, 1] = list[index, 1]
                    sublist_train.append((list[index, 0], list[index, 1]))
                    np.delete(list, index)
                    found = True
                else: index += 1
        indexBuch += 1

    indexBuch = 0
    for let in buchstaben: #für jeden buchstaben
        for count in range(size_eval): #jeder buchstabe wird x mal gebraucht
            index = 0
            found = False
            while (found is not True and index < len(list)):
                if(int(list[index,1]) == indexBuch):
                    #sublist[s_index, 0] = list[index, 0]
                    #sublist[s_index, 1] = list[index, 1]
                    sublist_eval.append((list[index, 0], list[index, 1]))
                    np.delete(list, index)
                    found = True
                else: index += 1
        indexBuch += 1

    indexBuch = 0
    for let in buchstaben: #für jeden buchstaben
        for count in range(size_test): #jeder buchstabe wird x mal gebraucht
            index = 0
            found = False
            while (found is not True and index < len(list)):
                if(int(list[index,1]) == indexBuch):
                    #sublist[s_index, 0] = list[index, 0]
                    #sublist[s_index, 1] = list[index, 1]
                    sublist_test.append((list[index, 0], list[index, 1]))
                    np.delete(list, index)
                    found = True
                else: index += 1
        indexBuch += 1

    np.random.shuffle(sublist_train)
    np.random.shuffle(sublist_eval)
    np.random.shuffle(sublist_test)

    return np.asarray(sublist_train), np.asarray(sublist_eval), np.asarray(sublist_test)


def set_all_datasets():
    train_img = tf.data.Dataset.from_generator(generator=generator_train_img, output_types=(tf.float32, tf.string))
    eval_img = tf.data.Dataset.from_generator(generator=generator_eval_img, output_types=(tf.float32, tf.string))
    test_img = tf.data.Dataset.from_generator(generator=generator_test_img, output_types=(tf.float32, tf.string))
    train_label = tf.data.Dataset.from_generator(generator=generator_train_label, output_types=(tf.float32, tf.string))
    eval_label = tf.data.Dataset.from_generator(generator=generator_eval_label, output_types=(tf.float32, tf.string))
    test_label = tf.data.Dataset.from_generator(generator=generator_test_label, output_types=(tf.float32, tf.string))
    # train = tf.data.Dataset.from_tensor_slices(sublist_train)
    # eval = tf.data.Dataset.from_tensor_slices(sublist_eval)
    # test = tf.data.Dataset.from_tensor_slices(sublist_test)

    return train_img, eval_img, test_img, train_label, eval_label, test_label


class TraicyData:

    train_img = None
    eval_img = None
    test_img = None
    train_label = None
    eval_label = None
    test_label = None

    def __init__(self, train_img=None, eval_img=None, test_img=None, train_label=None, eval_label=None, test_label=None):
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


def parse_data():
    global sublist_train, sublist_eval, sublist_test

    lists = load_all_data()
    sublist_train, sublist_eval, sublist_test = get_sublist(lists, 30, 30, 30)  # 1923, 385, 140
                                                                                # 49.998 Trainingsdaten,
                                                                                # 10010 Evaluierungsdaten,
                                                                                # 3640 Testdaten
    train_img, eval_img, test_img, train_label, eval_label, test_label = set_all_datasets() # funktioniert das??
    td = TraicyData(train_img, eval_img, test_img, train_label, eval_label, test_label)

    return td


def parse_data_as_array():
    global sublist_train, sublist_eval, sublist_test

    lists = load_all_data()
    sublist_train, sublist_eval, sublist_test = get_sublist(lists, 30, 30, 30)  # 1923, 385, 140
                                                                                # 49.998 Trainingsdaten,
                                                                                # 10010 Evaluierungsdaten,
                                                                                # 3640 Testdaten

    print (str(len(lists)) + " sublists: " + str(len(sublist_train)))

    train_img = np.asarray(list(generator_train_img()), dtype=np.float32)
    eval_img = np.asarray(list(generator_eval_img()), dtype=np.float32)
    test_img = np.asarray(list(generator_test_img()), dtype=np.float32)
    train_label = np.asarray(list(generator_train_label()), dtype=np.int32)
    eval_label = np.asarray(list(generator_eval_label()), dtype=np.int32)
    test_label = np.asarray(list(generator_test_label()), dtype=np.int32)

    return train_img, eval_img, test_img, train_label, eval_label, test_label


#train_img, eval_img, test_img, train_label, eval_label, test_label = parse_data_as_array()

#print(next(generator_train_img()))

# traicy = parse_data()
# iterator = traicy.test_img.make_one_shot_iterator()
# iterValue = iterator.get_next()
#
# sess = tf.Session()
# print(sess.run(iterValue))
