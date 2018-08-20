import tensorflow as tf
import initialize_dataset

training_data_file = "trai.cy"


def convolution(layer, filters):
    """
    Creates a convolutional layer with a number of filters on a 5x5 field
    :param layer: input tensor
    :param filters: count of filters to apply
    :return: convolutional layer tensor
    """
    # Convolutional Layer
    conv = tf.layers.conv2d(
        inputs=layer,
        filters=filters,
        kernel_size=[5, 5],
        padding="same",
        activation=tf.nn.relu)
    return conv


def pooling(layer, pool_size, strides):
    """
    Creates a pooling layer
    :param layer: input tensor
    :param pool_size: reduction rate, 2 = half the size
    :param strides: reduction type, 2 = use every second value
    :return: pooling layer tensor
    """
    # Pooling Layer
    pool = tf.layers.max_pooling2d(inputs=layer, pool_size=[pool_size, pool_size], strides=strides)
    return pool


def densely_connected(layer, size, neurons):
    """
    Creates a densely connected layer
    :param layer: input tensor
    :param size: size of how many features have been extracted
    :param neurons: count of neuron that connect all the data
    :return: densely connected layer tensor
    """
    # Dense Layer
    layer_flat = tf.reshape(layer, [-1, size])  # resize to match neuron count
    dense = tf.layers.dense(inputs=layer_flat, units=neurons, activation=tf.nn.relu)
    return dense


def dropout_layer(layer, rate,  mode):
    """
    Creates a dropout layer
    :param layer: input tensor
    :param rate: dropout rate, 0.4 = keep the 40% best neurons
    :param mode: mode when dropout should take effect (always training)
    :return: dropout layer tensor
    """
    # Dropout layer
    dropout = tf.layers.dropout(
        inputs=layer, rate=rate, training=mode == tf.estimator.ModeKeys.TRAIN)
    return dropout


def logits_layer(layer, units):
    """
    Creates a logits layer (densely connected)
    :param layer: input tensor
    :param units: count of categories to learn
    :return: logits layer tensor
    """
    # Logits Layer
    logits = tf.layers.dense(inputs=layer, units=units)
    return logits


def cnn_model_fn(features, labels, mode):
    """Model function for CNN"""

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

    # Convolutional Layer #3
    conv3 = convolution(pool2, 128)     # different to number prediction

    # Pooling Layer #3
    pool3 = pooling(conv3, 2, 2)        # different to number prediction

    # Dense Layer
    dense = densely_connected(pool3, 3 * 3 * 128, 1024)     # different to number prediction

    # Dropout layer
    dropout = dropout_layer(dense, 0.4, mode)

    # Logits Layer
    logits = tf.layers.dense(inputs=dropout, units=6)       # different to number prediction

    loss = None
    predictions = None
    eval_metric_ops = None
    train_op = None

    # return argument when predicting
    prediction_dict = {
        'class_ids': tf.argmax(input=logits, axis=1),
        'probabilities': tf.nn.softmax(logits, name="softmax_tensor"),
        'logits': logits,
    }

    if mode == tf.estimator.ModeKeys.EVAL:
        # Calculate Loss (for both TRAIN and EVAL modes)
        loss = tf.losses.sparse_softmax_cross_entropy(labels=labels, logits=logits)

        # Add evaluation metrics (for EVAL mode)
        eval_metric_ops = {
            "accuracy": tf.metrics.accuracy(labels=labels, predictions=prediction_dict["class_ids"])
        }

    if mode == tf.estimator.ModeKeys.TRAIN:
        # Calculate Loss (for both TRAIN and EVAL modes)
        loss = tf.losses.sparse_softmax_cross_entropy(labels=labels, logits=logits)

        # Configure the Training Op (for TRAIN mode)
        optimizer = tf.train.AdamOptimizer(learning_rate=1e-4)
        train_op = optimizer.minimize(
            loss=loss,
            global_step=tf.train.get_global_step())

    if mode == tf.estimator.ModeKeys.PREDICT:
        predictions = prediction_dict
        # return tf.estimator.EstimatorSpec(mode, predictions=predictions)

    return tf.estimator.EstimatorSpec(
        mode=mode,
        predictions=predictions,
        loss=loss,
        train_op=train_op,
        eval_metric_ops=eval_metric_ops)


def main():
    """
    Loads all training data, starts training and evaluates the training cycle
    """
    # Load training, eval and test data
    traicy_data = initialize_dataset.read_datafile(training_data_file)

    train_data = traicy_data.train_img
    eval_data = traicy_data.eval_img
    train_labels = traicy_data.train_label
    eval_labels = traicy_data.eval_label

    # Create the Estimator
    mnist_classifier = tf.estimator.Estimator(
        model_fn=cnn_model_fn, model_dir="./model_letter")

    # steps
    training_steps = 1000
    logging_steps = int(training_steps / 100)

    # Set up logging for predictions
    tensors_to_log = ['softmax_tensor']

    logging_hook = tf.train.LoggingTensorHook(
        tensors=tensors_to_log, every_n_iter=logging_steps)

    # Train the model_number
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

    # Evaluate the model_number and print results
    eval_input_fn = tf.estimator.inputs.numpy_input_fn(
        x={"x": eval_data},
        y=eval_labels,
        num_epochs=1,
        shuffle=False)

    # Evaluate training
    eval_results = mnist_classifier.evaluate(input_fn=eval_input_fn)
    print(eval_results)

    result = mnist_classifier.predict(input_fn=get_prediction_fn)
    print(str(result) + "  ||  " + str(result is not None))

    generator_result = next(result)
    generator_result_list_prob = list(x for x in generator_result['probabilities'])

    for i in generator_result_list_prob:
        print("{:.10f}".format(i*100))

    print("class id: " + str(generator_result['class_ids']))


def get_prediction_fn():
    """
    Input function for the prediction.
    Uses the provided test data to create the input dictionary
    :return: tuple of an image and a None label
    """

    traicy_data = initialize_dataset.read_datafile(training_data_file)
    test_data = traicy_data.test_img

    features = {'x': test_data[0].flatten()}
    labels = None

    return features, labels


class TraicyData:
    """
    Class for handling serialized TraicyData
    """

    train_img = None
    eval_img = None
    test_img = None
    train_label = None
    eval_label = None
    test_label = None

    def __init__(self, train_img=None, eval_img=None, test_img=None,
                 train_label=None, eval_label=None, test_label=None):
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


if __name__ == "__main__":
    # Enable logging
    tf.logging.set_verbosity(tf.logging.INFO)

    # start program
    tf.app.run(main)
