import numpy as np
import tensorflow as tf
from skimage.io import imread
from skimage.util import img_as_float
from os.path import abspath
import train_model_with_fully_custom_estimator

static_image_reference = None
model_dir = "./model"


def main():
    mnist_classifier = tf.estimator.Estimator(model_fn=train_model_with_fully_custom_estimator.cnn_model_fn,
                                              model_dir=model_dir)

    generator_result = None
    image_list = load_cust_images()

    print(len(image_list))

    for image in image_list:
        global static_image_reference
        static_image_reference = image # image_list[0]
        generator_result = mnist_classifier.predict(input_fn=prediction_image_fn)

    print_generator_content(generator_result)


def predict_image(image):
    mnist_classifier = tf.estimator.Estimator(model_fn=train_model_with_fully_custom_estimator.cnn_model_fn,
                                              model_dir=model_dir)
    global static_image_reference
    static_image_reference = image  # image_list[0]

    generator_result = mnist_classifier.predict(input_fn=prediction_image_fn)
    number, confidence = extract_prediction_result(next(generator_result))

    return number, confidence


def prediction_image_fn():
    if static_image_reference is not None:

        features = {'x': static_image_reference.flatten()}
        labels = None

        return features, labels
    else:
        return None


def load_cust_images():
    image_list = list()

    path = abspath(__file__ + "/../../")
    data_path = str(path) + "/data/"

    for index in range(0, 10):
        read_img = imread(data_path + f"images_human_skeleton/{index}.png", as_grey=True)
        img_flat = img_as_float(read_img.flatten().reshape(1, 784))
        img_flat_f32 = img_flat.astype(np.float32, copy=True)

        image_list.append(img_flat_f32)

    return image_list


def extract_prediction_result(generator_content):
    best_category_index = generator_content['class_ids']
    best_category_confidence = generator_content['probabilities'][best_category_index]

    return best_category_index, best_category_confidence


def print_generator_content(generator):
    if generator is not None:

        while True:
            generator_results = next(generator)

            if generator_results is None:
                break
            else:
                generator_result_list = list(x for x in generator_results['probabilities'])
                for i in generator_result_list:
                    print("{:.10f}".format(i * 100))
                print('\n')


if __name__ == "__main__":
    main()
