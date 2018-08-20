import exifread
from cv2.cv2 import rotate


def rotate_image(img_read, rotation):
    """
        Rotates a given image by a given rotation clock wise

        :parameter
            img_read: binary image array
            rotation: Rotation clock wise in degree

        :returns
            array of the new rotated image
    """
    if rotation is not None:
        rotate_value = (str.split(str(rotation), " ")[1])
        if isinstance(rotate_value, int) or isinstance(rotate_value, float):
            value_cw = -float(rotate_value)
            img_rotated = rotate(img_read, value_cw)
            return img_rotated
        else:
            return img_read
    else:
        return img_read


def get_image_rotation_from_location(directory):
    """
        Get the Image Orientation Tag from an image and return it

        :parameter
            filename: name of the original image

        :returns
            EXIF file tag if it exists
    """

    file = open(directory, 'rb')
    tags = exifread.process_file(file)

    for tag in tags.keys():
        if tag == 'Image Orientation':
            return tags[tag]


def get_image_rotation(filename, folder):
    """
        Get the Image Orientation Tag from an image and return it

        :parameter
            filename: name of the original image

        :returns
            EXIF file tag if it exists
    """

    file = open(folder + filename, 'rb')
    tags = exifread.process_file(file)

    for tag in tags.keys():
        if tag == 'Image Orientation':
            return tags[tag]