import numpy as np
import tensorflow as tf
from skimage.io import imread
from tensorflow.examples.tutorials.mnist import input_data
from os.path import abspath


def weight_variable(shape):
    """
    Creates and returns a new weight variable
        :param shape: desired shape of the variable

        :return: a new weight variable of a certain shape
    """
    initial = tf.truncated_normal(shape, stddev=0.1)
    return tf.Variable(initial)


def bias_variable(shape):
    """
    Creates and returns a new bias variable
        :param shape: desired shape of the variable

        :return a new bias variable of a certain shape
    """
    initial = tf.constant(0.1, shape=shape)
    return tf.Variable(initial)


def conv2d(x, W):
    """
    Convolutes a given 4D Tensor into a 2D Tensor
        :param x: Tensor to be convoluted
        :param W: Filter Tensor giving the shape of the returning Tensor

        :return a convoluted 2D Tensor with the shape of W
    """
    return tf.nn.conv2d(x, W, strides=[1, 1, 1, 1], padding='SAME')


def max_pool_2x2(x):
    """
    Convolutes a given 4D Tensor into a 2D Tensor
        :param x: Tensor to be convoluted
        :param W: Filter Tensor giving the shape of the returning Tensor

        :return a convoluted 2D Tensor with the shape of W
    """
    return tf.nn.max_pool(x, ksize=[1, 2, 2, 1], strides=[1, 2, 2, 1], padding='SAME')


def first_c_layer(x):
    """
    Creates the first layer of the CNN
        :param x: Tensor the layer is attached to
        :return: Tensor following layers are attached to
    """
    W_conv1 = weight_variable([5, 5, 1, 32])
    b_conv1 = bias_variable([32])
    x_image = tf.reshape(x, [-1, 28, 28, 1])
    h_conv1 = tf.nn.relu(conv2d(x_image, W_conv1) + b_conv1)
    h_pool1 = max_pool_2x2(h_conv1)
    return h_pool1


def second_c_layer(h_pool1):
    """
    Creates the second layer of the CNN
        :param h_pool1: Tensor the layer is attached to
        :return: Tensor following layers are attached to
    """
    W_conv2 = weight_variable([5, 5, 32, 64])
    b_conv2 = bias_variable([64])

    h_conv2 = tf.nn.relu(conv2d(h_pool1, W_conv2) + b_conv2)
    h_pool2 = max_pool_2x2(h_conv2)
    return h_pool2


def dense_con_layer(h_pool2):
    """
    Creates the densly connected layer of the CNN
        :param h_pool2: Tensor the layer is attached to
        :return: Tensor following layers are attached to
    """
    W_fc1 = weight_variable([7 * 7 * 64, 1024])
    b_fc1 = bias_variable([1024])

    h_pool2_flat = tf.reshape(h_pool2, [-1, 7 * 7 * 64])
    h_fc1 = tf.nn.relu(tf.matmul(h_pool2_flat, W_fc1) + b_fc1)
    return h_fc1


def dropout_layer(h_fc1):
    """
    Creates the dropout layer of the CNN
        :param h_fc1: Tensor the layer is attached to
        :return: Tensor following layers are attached to and the probability of a node being kept in the next iteration
    """
    keep_prob = tf.placeholder(tf.float32, name="keep_prob")
    h_fc1_drop = tf.nn.dropout(h_fc1, keep_prob)
    return h_fc1_drop, keep_prob


def readout_layer(h_fc1_drop):
    """
    Creates the readout of the CNN
        :param h_fc1_drop: Tensor the layer is attached to
        :return: Tensor that can be evaluated to get the prediction results
    """
    W_fc2 = weight_variable([1024, 10])
    b_fc2 = bias_variable([10])

    y_conv = tf.matmul(h_fc1_drop, W_fc2) + b_fc2
    return y_conv


def create_network(x):
    """
    Creates the neural network
        :param x: Input Tensor for the image
        :return: last Tensor of the network and the keep propability
    """
    first = first_c_layer(x)
    second = second_c_layer(first)
    dense = dense_con_layer(second)
    drop, keep_prob = dropout_layer(dense)
    read = readout_layer(drop)
    return read, keep_prob


def training_variables(net, y_):
    """
    Creates the training variables
        :param net: network architecture
        :param y_: Output Tensor for the prediction
        :return: training variables
    """
    cross_entropy = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits(labels=y_, logits=net))
    train_step = tf.train.AdamOptimizer(1e-4).minimize(cross_entropy)
    correct_prediction = tf.equal(tf.argmax(net, 1), tf.argmax(y_, 1))
    accuracy = tf.reduce_mean(tf.cast(correct_prediction, tf.float32), name='accuracy')

    return cross_entropy, train_step, correct_prediction, accuracy


def start_training(mnist, accuracy, train_step, keep_prob, x, y_):
    """
    Starts the training process
        :param mnist: training data
        :param accuracy: last operation in network, used for evaluation
        :param train_step: optimizer for each training step
        :param keep_prob: probability to keep a node
        :param x: Input tensor
        :param y_: Output Tensor
    """
    with tf.Session() as sess:

        sess.run(tf.global_variables_initializer())
        saver = tf.train.Saver(save_relative_paths=True)

        for i in range(10000):
            batch = mnist.train.next_batch(50)
            if i % 100 == 0:
                train_accuracy = accuracy.eval(feed_dict={
                    x: batch[0], y_: batch[1], keep_prob: 1.0})
                print('step %d, training accuracy %g' % (i, train_accuracy))
            train_step.run(feed_dict={x: batch[0], y_: batch[1], keep_prob: 0.5})

        print('test accuracy %g' % accuracy.eval(feed_dict={
            x: mnist.test.images, y_: mnist.test.labels, keep_prob: 1.0}))

        save_model(sess, saver)

        image_list = load_cust_images()
        counter = 0
        for i in image_list:
            predict(i, accuracy, x, y_, keep_prob, counter)
            counter += 1


def save_model(sess, saver):
    """
    Saves a TensorFlow session into a model
    """
    saver.save(sess, "./model/CNN_MNIST")


def predict(img_flat, accuracy, x, y_, keep_prob, actual):
    """
        Predicts a number in a given image and prints the result
            :param img_flat: image to analyze
            :param accuracy: last operation in network, used for evaluation
            :param x: Input Tensor for the prediction
            :param y_: Output Tensor for the prediction
            :param keep_prob: probability to keep a node
            :param actual: actual number
    """

    dict_poss = create_poss()

    for i in range(0, len(dict_poss)):
        prediction = accuracy.eval(feed_dict={x: img_flat, y_: dict_poss[i].reshape(1, 10), keep_prob: 1.0})
        if prediction - 0.5 > 0:
            print(f"Guessing with {prediction} prob. for {round(i, 2)} while its {round(actual, 2)}")


def create_poss():
    """
    Creates an array of possible answers
        :return: array of possible answers
    """
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
    return dict_poss


def load_cust_images():
    """
        Loads a bulk of images and returns them as a list
        :return: list of loaded images
    """
    image_list = list()

    path = abspath(__file__ + "/../../")
    data_path = str(path) + "/data/"

    for index in range(0, 10):
        read_img = imread(data_path + f"images_human_skeleton/{index}.png", as_grey=True)
        img_flat = read_img.flatten().reshape(1, 784)

        image_list.append(img_flat)

    return image_list


# START PROGRAM
def main():
    """
        Starts the training process
    """
    mnist = input_data.read_data_sets('MNIST_data', one_hot=True)

    x = tf.placeholder(tf.float32, [None, 784], name='x')
    y_ = tf.placeholder(tf.float32, [None, 10], name='y_')

    net, keep_prob = create_network(x)
    cross_entropy, train_step, correct_prediction, accuracy = training_variables(net, y_)

    start_training(mnist, accuracy, train_step, keep_prob, x, y_)


if __name__ == "__main__":
    main()


