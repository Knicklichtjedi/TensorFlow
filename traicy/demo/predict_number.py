import ImageFilter
import CNN_load_model
import sys

image_path = sys.argv[1]

if image_path is not None:
    img_com = ImageFilter.read_image_from_location(image_path)
    number, confidence = CNN_load_model.predict_image(img_com)

    print(str(number) + "," + str(confidence))

