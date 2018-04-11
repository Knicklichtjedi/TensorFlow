import numpy as np
import tensorflow as tf
from skimage.io import imread
from skimage.util import img_as_float
from os.path import abspath

def create_poss():
    a0 = np.array([1, 0, 0, 0, 0, 0, 0, 0, 0, 0])
    a1 = np.array([0, 1, 0, 0, 0, 0, 0, 0, 0, 0])
    a2 = np.array([0, 0, 1, 0, 0, 0, 0, 0, 0, 0])
    a3 = np.array([0, 0, 0, 1, 0, 0, 0, 0, 0, 0])
    a4 = np.array([0, 0, 0, 0, 1, 0, 0, 0, 0, 0])
    a5 = np.array([0, 0, 0, 0, 0, 1, 0, 0, 0, 0])
    a6 = np.array([0, 0, 0, 0, 0, 0, 1, 0, 0, 0])
    a7 = np.array([0, 0, 0, 0, 0, 0, 0, 1, 0, 0])
    a8 = np.array([0, 0, 0, 0, 0, 0, 0, 0, 1, 0])
    a9 = np.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 1])

    dict_poss = np.array([a0, a1, a2, a3, a4, a5, a6, a7, a8, a9])
    return img_as_float(dict_poss)


def load_cust_images():
    image_list = list()

    path = abspath(__file__ + "/../../")
    data_path = str(path) + "/data/"

    for index in range(0, 10):
        read_img = imread(data_path + f"images_human_skeleton/{index}.png", as_grey=True)
        img_flat = img_as_float(read_img.flatten().reshape(1, 784))

        image_list.append(img_flat)

    return image_list


def predict(img_flat, accuracy, x, y_, keep_prob, actual):
    # with tf.Session() as sess:

        # sess.run(tf.global_variables_initializer())
        dict_poss = create_poss()

        # for i in range(0, len(dict_poss)):
        #   prediction = sess.run(tf.global_variables_initializer(),
        #                               feed_dict={ x: img_flat,
        #                                           y_: dict_poss[i].reshape(1, 10),
        #                                           keep_prob: 1.0})
        #   if prediction > 0.5: print("Guessing: " + str(prediction) + " " + str(i))

        for i in range(0, len(dict_poss)):
            prediction = accuracy.eval(feed_dict={x: img_flat, y_: dict_poss[i].reshape(1, 10), keep_prob: 1.0})
            if prediction - 0.5 > 0:
                print(f"Guessing with {prediction} prob. for {round(i, 2)} while its {round(actual, 2)}")


def predict_image(img):
    with tf.Session() as sess:

        saver = tf.train.import_meta_graph('./model/CNN_MNIST.meta')
        saver.restore(sess, tf.train.latest_checkpoint('./model/'))

        graph = tf.get_default_graph()
        x = graph.get_tensor_by_name("x:0")
        y_ = graph.get_tensor_by_name("y_:0")
        keep_prob = graph.get_tensor_by_name("keep_prob:0")

        op = graph.get_tensor_by_name("accuracy:0")

        dict_poss = create_poss()

        for index in range(0, len(dict_poss)):
            prediction = op.eval(feed_dict={x: img, y_: dict_poss[index].reshape(1, 10), keep_prob: 1.0})
            if prediction - 0.5 > 0:
                return str(round(index, 2)), str(prediction)
                # print(f"Guessing with {prediction} prob. for {round(index, 2)} while its {round(counter, 2)}")


def main():
    # tf.reset_default_graph()

    # x = tf.placeholder(tf.float32, [None, 784], name='x')
    # y_ = tf.placeholder(tf.float32, [None, 10], name='y_')
    # accuracy = tf.placeholder(tf.float32, [None, 10], name='accuracy')

    # x = tf.get_variable("x", [1])
    # y_ = tf.get_variable("y_", [1])
    # accuracy = tf.get_variable("accuracy", [1])

    # var = tf.get_variable("Variable_7/Adam_1", [10])
    # x = tf.placeholder(tf.float32, [1, 784], name='x')
    # y_ = tf.placeholder(tf.float32, [1, 10], name='y_')
    # keep_prob = tf.placeholder(tf.float32)

    with tf.Session() as sess:

        # saver = tf.train.import_meta_graph('model/CNN_MNIST.meta')
        # saver.restore(sess, save_path='model/CNN_MNIST')
        # print(sess.run('x:0'))

        saver = tf.train.import_meta_graph('./model/CNN_MNIST.meta')
        saver.restore(sess, tf.train.latest_checkpoint('./model/'))

        # print(sess.run('bias:0'))

        graph = tf.get_default_graph()
        x = graph.get_tensor_by_name("x:0")
        y_ = graph.get_tensor_by_name("y_:0")
        keep_prob = graph.get_tensor_by_name("keep_prob:0")

        op = graph.get_tensor_by_name("accuracy:0")

        # [op for op in tf.get_default_graph().get_operations() if op.type ]

        # saver.restore(sess, "model/CNN_MNIST.ckpt")
        # sess.run(tf.global_variables_initializer())
        # graph = tf.get_default_graph()
        # accuracy = graph.get_tensor_by_name('accuracy:0')
        #
        # acc = sess.run(accuracy)
        #
        # print(acc)

        image_list = load_cust_images()
        dict_poss = create_poss()
        counter = 0
        for i in image_list:
            # feed_dict = {x: i, y_: dict_poss[counter].reshape(1, 10), keep_prob: 1.0}
            # print(sess.run(op, feed_dict))

            for index in range(0, len(dict_poss)):
                prediction = op.eval(feed_dict={x: i, y_: dict_poss[index].reshape(1, 10), keep_prob: 1.0})
                if prediction - 0.5 > 0:
                    print(f"Guessing with {prediction} prob. for {round(index, 2)} while its {round(counter, 2)}")
            counter += 1


if __name__ == "__main__":
    main()

# ######################################### HUMAN SKELETON

# TRAINING
# Guessing with 1.0 prob. for 9 while its 0
# Guessing with 1.0 prob. for 1 while its 1
# Guessing with 1.0 prob. for 7 while its 2
# Guessing with 1.0 prob. for 3 while its 3
# Guessing with 1.0 prob. for 4 while its 4
# Guessing with 1.0 prob. for 5 while its 5
# Guessing with 1.0 prob. for 1 while its 6
# Guessing with 1.0 prob. for 7 while its 7
# Guessing with 1.0 prob. for 2 while its 8
# Guessing with 1.0 prob. for 9 while its 9

# ######################################### HUMAN SKELETON

# LOADED
# Guessing with 1.0 prob. for 9 while its 0
# Guessing with 1.0 prob. for 1 while its 1
# Guessing with 1.0 prob. for 7 while its 2
# Guessing with 1.0 prob. for 3 while its 3
# Guessing with 1.0 prob. for 4 while its 4
# Guessing with 1.0 prob. for 5 while its 5
# Guessing with 1.0 prob. for 1 while its 6
# Guessing with 1.0 prob. for 7 while its 7
# Guessing with 1.0 prob. for 2 while its 8
# Guessing with 1.0 prob. for 7 while its 9

# ######################################### EVA

# TRAINING
# Guessing with 1.0 prob. for 0 while its 0
# Guessing with 1.0 prob. for 7 while its 1
# Guessing with 1.0 prob. for 2 while its 2
# Guessing with 1.0 prob. for 3 while its 3
# Guessing with 1.0 prob. for 4 while its 4
# Guessing with 1.0 prob. for 5 while its 5
# Guessing with 1.0 prob. for 6 while its 6
# Guessing with 1.0 prob. for 7 while its 7
# Guessing with 1.0 prob. for 8 while its 8
# Guessing with 1.0 prob. for 3 while its 9

# ######################################### EVA

# LOADED
# Guessing with 1.0 prob. for 0 while its 0
# Guessing with 1.0 prob. for 7 while its 1
# Guessing with 1.0 prob. for 2 while its 2
# Guessing with 1.0 prob. for 3 while its 3
# Guessing with 1.0 prob. for 4 while its 4
# Guessing with 1.0 prob. for 5 while its 5
# Guessing with 1.0 prob. for 6 while its 6
# Guessing with 1.0 prob. for 7 while its 7
# Guessing with 1.0 prob. for 8 while its 8
# Guessing with 1.0 prob. for 3 while its 9
