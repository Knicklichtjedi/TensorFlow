import numpy as np
import tensorflow as tf
from skimage.io import imread
from tensorflow.examples.tutorials.mnist import input_data
from os.path import abspath
import random


def convolution(layer, filters):
    # Convolutional Layer
    conv = tf.layers.conv2d(
        inputs=layer,
        filters=filters,
        kernel_size=[5, 5],
        padding="same",
        activation=tf.nn.relu)
    return conv


def pooling(layer, pool_size, strides):
    # Pooling Layer
    pool = tf.layers.max_pooling2d(inputs=layer, pool_size=[pool_size, pool_size], strides=strides)
    return pool


def densely_connected(layer, size, neurons):
    # Dense Layer
    layer_flat = tf.reshape(layer, [-1, size])
    dense = tf.layers.dense(inputs=layer_flat, units=neurons, activation=tf.nn.relu)
    return dense


def dropout_layer(layer, rate,  mode):
    # Dropout layer
    dropout = tf.layers.dropout(
        inputs=layer, rate=rate, training=mode == tf.estimator.ModeKeys.TRAIN)
    return dropout


def logits_layer(layer, units):
    # Logits Layer
    logits = tf.layers.dense(inputs=layer, units=units)
    return logits


def cnn_model_fn(features, labels, mode):
    """Model function for CNN."""

    # Input Layer
    input_layer = tf.reshape(features["x"], [-1, 28, 28, 1])

    # Convolutional Layer #1
    conv1 = convolution(input_layer, 32)

    # Pooling Layer #1
    pool1 = pooling(conv1, 2, 2)

    # Convolutional Layer #2
    conv2 = convolution(pool1, 64)

    # Pooling Layer #2
    pool2 = pooling(conv2, 2, 2)

    # Dense Layer
    dense = densely_connected(pool2, 7 * 7 * 64, 1024)

    # Dropout layer
    dropout = dropout_layer(dense, 0.4, mode)

    # Logits Layer
    logits = tf.layers.dense(inputs=dropout, units=10)

    # dictionary
    # predictions = {
    #     # Generate predictions (for PREDICT and EVAL mode)
    #     "classes": tf.argmax(input=logits, axis=1, name="class_tensor"),
    #     # Add `softmax_tensor` to the graph. It is used for PREDICT and by the
    #     # `logging_hook`.
    #     "probabilities": tf.nn.softmax(logits, name="softmax_tensor")
    # }
    #
    # prediction_tensor = tf.nn.softmax(logits, name="softmax_only_tensor")

    prediction_dict = {
            'class_ids': tf.argmax(input=logits, axis=1),
            'probabilities': tf.nn.softmax(logits, name="softmax_tensor"),
            'logits': logits,
    }

    # onehot_labels = tf.one_hot(indices=tf.cast(labels, tf.int32), depth=10)
    # loss = tf.losses.softmax_cross_entropy(onehot_labels=onehot_labels, logits=logits)

    # Calculate Loss (for both TRAIN and EVAL modes)
    loss = tf.losses.sparse_softmax_cross_entropy(labels=labels, logits=logits)

    # loss = tf.nn.softmax_cross_entropy_with_logits_v2(labels=labels, logits=logits)

    # Configure the Training Op (for TRAIN mode
    #if mode == tf.estimator.ModeKeys.TRAIN:
    #    optimizer = tf.train.AdamOptimizer(learning_rate=1e-4)
    #    train_op = optimizer.minimize(
    #        loss=loss,
    #        global_step=tf.train.get_global_step())
    #    return tf.estimator.EstimatorSpec(mode=mode, loss=loss, train_op=train_op)
    #
    #if mode == tf.estimator.ModeKeys.PREDICT:
    #    return tf.estimator.EstimatorSpec(mode=mode, predictions=predictions)
    #
    # Add evaluation metrics (for EVAL mode)
    #eval_metric_ops = {
    #    "accuracy": tf.metrics.accuracy(
    #     labels=labels, predictions=predictions["classes"])}
    #
    #return tf.estimator.EstimatorSpec(
    #  mode=mode, loss=loss, eval_metric_ops=eval_metric_ops)

    eval_metric_ops = {
       "accuracy": tf.metrics.accuracy(
        labels=labels, predictions=prediction_dict["class_ids"])}

    if mode == tf.estimator.ModeKeys.EVAL:
        loss = loss
        eval_metric_ops = eval_metric_ops
    else:
        pass
        # loss = None
        # eval_metric_ops = None

    if mode == tf.estimator.ModeKeys.TRAIN:
        optimizer = tf.train.AdamOptimizer(learning_rate=1e-4)
        # optimizer = tf.train.GradientDescentOptimizer(learning_rate=0.05)
        train_op = optimizer.minimize(
            loss=loss,
            global_step=tf.train.get_global_step())
    else:
        pass
        train_op = None
        # eval_metric_ops = None

    if mode == tf.estimator.ModeKeys.PREDICT:
        predictions = prediction_dict
        # return tf.estimator.EstimatorSpec(mode, predictions=predictions)
    else:
        predictions = None

    return tf.estimator.EstimatorSpec(
        mode=mode,
        predictions=predictions,
        loss=loss,
        train_op=train_op,
        eval_metric_ops=eval_metric_ops)


def main(argv):
    # Load training and eval data
    mnist = tf.contrib.learn.datasets.load_dataset("mnist")
    train_data = mnist.train.images                                 # Returns np.array
    train_labels = np.asarray(mnist.train.labels, dtype=np.int32)
    eval_data = mnist.test.images                                   # Returns np.array
    eval_labels = np.asarray(mnist.test.labels, dtype=np.int32)

    # Create the Estimator
    mnist_classifier = tf.estimator.Estimator(
        model_fn=cnn_model_fn, model_dir="./model/mnist_convnet_model")

    # steps
    training_steps = 200
    logging_steps = int(training_steps / 100)

    # Set up logging for predictions
    tensors_to_log = ['softmax_tensor']
    # {"probabilities": "softmax_tensor"} , "classes": "class_tensor"

    logging_hook = tf.train.LoggingTensorHook(
        tensors=tensors_to_log, every_n_iter=logging_steps)

    # Train the model
    train_input_fn = tf.estimator.inputs.numpy_input_fn(
        x={"x": train_data},
        y=train_labels,
        batch_size=100,
        num_epochs=None,
        shuffle=True)

    mnist_classifier.train(
        input_fn=train_input_fn,
        steps=training_steps,
        hooks=[logging_hook])

    # Evaluate the model and print results
    eval_input_fn = tf.estimator.inputs.numpy_input_fn(
        x={"x": eval_data},
        y=eval_labels,
        num_epochs=1,
        shuffle=False)

    eval_results = mnist_classifier.evaluate(input_fn=eval_input_fn)
    print(eval_results)

    # test_image = eval_data[0].flatten()
    # test_dict = {"x": test_image}
    # input_fn = tf.estimator.inputs.numpy_input_fn(x=test_dict, y=test_labels, shuffle=False)
    # test_tuple = (10, test_image)

    # dataset = tf.data.Dataset.from_generator(get_prediction_image, tf.int64)

    random_label = random.randrange(0, 10)

    predict_image = tf.estimator.inputs.numpy_input_fn(
        x={"x": eval_data[0]},
        y=np.array(random_label),
        num_epochs=1,
        shuffle=False)

    print(str(random_label) + "  " + str(type(eval_labels[0])))

    result = mnist_classifier.predict(input_fn=predict_image)              # , predict_keys=['probabilities']

    print(str(result) + "  ||  " + str(result is not None))

    for i in iter(result):
        print(str(i))

    # expected = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    # for pred_dict, expec in zip(result, expected):
    #     class_id = pred_dict['classes'][0]
    #     probability = pred_dict['probabilities'][class_id]
    #     print(str(class_id) + " " + str(probability))

    # print(result)

    # iterator = iter(result)
    #
    # print(iterator)

    # for element in range(0, 10):
    #    print(next(iterator))

    # print(next(generator))
    # for element in list(result):
    #    print(element)

    # prediction = result['class_id'][0]
    # print(result['probabilities'][prediction])

    # print(list(result))


if __name__ == "__main__":
    # Enable logging
    tf.logging.set_verbosity(tf.logging.INFO)

    # start programm
    tf.app.run(main)
