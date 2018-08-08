import glob
import pickle
from os.path import abspath
from random import shuffle

import numpy as np
import tensorflow as tf

buchstaben = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z"]
file_list = [] #bilddateien
labels_list = []

sublist_train = []
sublist_eval = []
sublist_test = []

def generator_train():
    yield sublist_train


def generator_eval():
    yield sublist_eval

def generator_test():
    #images = np.array([784][1])
    #labels = np.array([1])
    #yield images, labels
    yield sublist_test

def load_all_data():
    #gives back lists
    ####SET PATHS####
    path = abspath(__file__ + "/../../")  # change directory to traicy
    traicy_data_path = path + "/cnn/TRAICY_data/"  # save in folder

    ####GET ALL FILES IN A LIST####
    for dir in buchstaben:
        directory = traicy_data_path + dir + "/"
        for filename in glob.glob(directory + '*.jpg'):  # only jpg
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

    return sublist_train, sublist_eval, sublist_test


def set_all_datasets():
    train = tf.data.Dataset.from_generator(generator=generator_train, output_types=(tf.int64, tf.int64))
    eval = tf.data.Dataset.from_generator(generator=generator_eval, output_types=(tf.int64, tf.int64))
    test = tf.data.Dataset.from_generator(generator=generator_test, output_types=(tf.int64, tf.int64))

    return train,eval,test


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


lists = load_all_data()
sublist_train, sublist_eval, sublist_test = get_sublist(lists, 30,30,30)#1923, 385, 140) #49.998 Trainingsdaten, 10010 Evaluierungsdaten, 3640 Testdaten
#print(sublist_test[0])

train, test, eval = set_all_datasets() #funktioniert das??
#print(train, test,eval)
#neues TraicyData erstellen mit train, test, eval
#serialisieren


#mnist = tf.contrib.learn.datasets.load_dataset("mnist")
#train_data = mnist.train.images                                 # Returns np.array
#train_labels = np.asarray(mnist.train.labels, dtype=np.int32)
#eval_data = mnist.test.images                                   # Returns np.array
#eval_labels = np.asarray(mnist.test.labels, dtype=np.int32)

#myData = TraicyData()
#myData.test = mnist.test
#myData.train = mnist.train

#file_save = open("ser.obj", "wb")
#pickle.dump(myData, file_save)

#file_load = open("ser.obj", "rb")
#myLoadedData = pickle.load(file_load)

#myLoadedTraicyData = TraicyData(myLoadedData.train, myLoadedData.test)

#print(type(myLoadedData))

#print(type(myLoadedTraicyData))
#print(myLoadedTraicyData.train.labels)

# myLoadedData = pickle.loads(data.encode("utf-8"))
#
# print(type(myLoadedData))


