import ImageFilter_noLoad
import CNN_load_model
import sys
from skimage import img_as_float

image_path = sys.argv[1]

if image_path is not None:
    # img_com = ImageFilter_noLoad.read_image_from_location(image_path)
    # img_flat = img_as_float(img_com.flatten().reshape(1, 784))

    # number, confidence = CNN_load_model.predict_image(img_flat)

    # print(str(number) + "," + str(confidence))

    img_list, coord_list = ImageFilter_noLoad.read_image_with_chunks_from_location(image_path)
    predictions = ""

    for image in img_list:

        img_flat = img_as_float(image.flatten().reshape(1, 784))

        number, confidence = CNN_load_model.predict_image(img_flat)

        predictions += (str(number) + ", " + str(confidence)) + "\n"

    print(predictions)
