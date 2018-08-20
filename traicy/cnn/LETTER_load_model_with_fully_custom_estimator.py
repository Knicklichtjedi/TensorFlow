import numpy as np
import tensorflow as tf
from skimage.io import imread
from skimage.util import img_as_float
from os.path import abspath
import LETTER_train_model_with_fully_custom_estimator
import glob

static_image_reference = None
model_dir = abspath("./python_resources/model_letter/")         # model dir when GUI uses script
model_dir_main = "./model_letter"                               # model dir when main() uses script

# possible categories
letters = ["T", "R", "A", "I", "C", "Y"]


def main():
    """
    Loads the model with a certain model function from a certain directory.
    Then loads custom images for the letter prediction.
    Prints the content of the prediction generator.
    """

    # load model
    mnist_classifier = tf.estimator.Estimator(model_fn=LETTER_train_model_with_fully_custom_estimator.cnn_model_fn,
                                              model_dir=model_dir)

    image_list = load_cust_images()

    for image in image_list:
        global static_image_reference
        static_image_reference = image
        generator_result = mnist_classifier.predict(input_fn=prediction_image_fn)

        print_generator_content(generator_result)


def predict_image(image):
    """
    Predicts a letter in an image and returns the results
    :param image: binary flat image (1x784) where the number is in
    :return: category (letter) and confidence of that prediction
    """

    # load model
    mnist_classifier = tf.estimator.Estimator(model_fn=LETTER_train_model_with_fully_custom_estimator.cnn_model_fn,
                                              model_dir=model_dir)
    global static_image_reference
    static_image_reference = image  # image_list[0]

    generator_result = mnist_classifier.predict(input_fn=prediction_image_fn)
    number, confidence = extract_prediction_result(next(generator_result))

    return number, confidence


def prediction_image_fn():
    """
    Input function for the prediction.
    Uses the static image reference to create the input dictionary
    :return: tuple of an image and a None label
    """

    if static_image_reference is not None:

        features = {'x': static_image_reference.flatten()}
        labels = None

        return features, labels
    else:
        return None


def load_cust_images():
    """
    Loads images from /data/images_letters/ an prepares them for prediction.
    Load, flatten, reshape (1x784) and convert to float32
    :return: list of prepared images
    """

    image_list = list()

    path = abspath(__file__ + "/../../")
    data_path = str(path) + "/data/images_letters/"

    for element in glob.glob(data_path + '*.png'):
        read_img = imread(element, as_grey=True)
        img_flat = img_as_float(read_img.flatten().reshape(1, 784))
        img_flat_f32 = img_flat.astype(np.float32, copy=True)

        image_list.append(img_flat_f32)

    return image_list


def extract_prediction_result(generator_content):
    """
    Extracts one prediction result from the generator
    :param generator_content: generator to extract data from
    :return: best category index and the corresponding confidence
    """

    best_category_index = generator_content['class_ids']
    best_category_confidence = generator_content['probabilities'][best_category_index]

    return best_category_index, best_category_confidence


def print_generator_content(generator, print_loop=False):
    """
    Prints all content of an letter prediction generator
    :param generator: generator to extract data from
    :param print_loop: if False the generator will only print one result
    """
    if generator is not None:

        keep_print_loop = True
        while keep_print_loop:
            generator_results = next(generator)

            if generator_results is None:
                break
            else:
                generator_result_list = list(x for x in generator_results['probabilities'])
                best_class_id = generator_results['class_ids']
                for index in range(0, len(generator_result_list)):
                    confidence = generator_result_list[index]
                    print("{}: {:.10f}".format(letters[index], confidence * 100))
                print("best: {} with {:.3f}".format(letters[best_class_id], generator_result_list[best_class_id] * 100))
                print('\n')

            keep_print_loop = print_loop


if __name__ == "__main__":
    main()
