from tensorflow.examples.tutorials.mnist import input_data
import matplotlib.pyplot as plt
import numpy as np
import random as ran
import tensorflow as tf

mnist = input_data.read_data_sets('MNIST_data', one_hot=True)


def TRAIN_SIZE(num):
    global x_train, y_train
    x_train = mnist.train.images[:num, :]
    y_train = mnist.train.labels[:num, :]
    return x_train, y_train


def TEST_SIZE(num):
    global x_train, y_train
    x_test = mnist.test.images[:num, :]
    y_test = mnist.test.labels[:num, :]
    return x_test, y_test


sess = tf.Session()

x = tf.placeholder(tf.float32, shape=[None, 784])   # Data input tensor
y_ = tf.placeholder(tf.float32, shape=[None, 10])   # Label input tensor

W = tf.Variable(tf.zeros([784, 10]))
b = tf.Variable(tf.zeros([10]))

softmax = tf.nn.softmax(tf.matmul(x, W) + b)
cross_entropy = tf.reduce_mean(-tf.reduce_sum(y_ * tf.log(softmax), reduction_indices=[1]))

x_train, y_train = TRAIN_SIZE(5000)
x_test, y_test = TEST_SIZE(200)
LEARNING_RATE = 0.1
TRAIN_STEPS = 2500

init = tf.global_variables_initializer()
sess.run(init)

training = tf.train.GradientDescentOptimizer(LEARNING_RATE).minimize(cross_entropy)
correct_prediction = tf.equal(tf.argmax(softmax, 1), tf.argmax(y_, 1))
accuracy = tf.reduce_mean(tf.cast(correct_prediction, tf.float32))

for i in range(TRAIN_STEPS+1):
    sess.run(training, feed_dict={x: x_train, y_: y_train})
    if i % 100 == 0:
        print('Training Step:' + str(i) + '  Accuracy =  ' + str(sess.run(accuracy, feed_dict={x: x_test, y_: y_test})) + '  Loss = ' + str(sess.run(cross_entropy, {x: x_train, y_: y_train})))

x_test, y_test = TEST_SIZE(1)

answer = sess.run(softmax, feed_dict={x: x_test})
answer_element = answer[0, answer.argmax()]
print(answer.argmax(), answer_element)


