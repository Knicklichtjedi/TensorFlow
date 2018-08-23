import numpy as np
from matplotlib.image import imsave
from skimage.color import rgb2gray, rgb2hsv, hsv2rgb


def clamp_float_values(img):
    """
    creates np array from image
    :param img: original image
    :return: np array
    """
    img_np_array = rgb2gray(np.array(img))
    h, w = img_np_array.shape

    for x in range(0, w):
        for y in range(0, h):
            if img_np_array[y, x] > 0:
                img_np_array[y, x] = 1
            else:
                img_np_array[y, x] = 0

    return img_np_array


def clamp_binary_values(img):
    """
    creates np array from image
    :param img: original image
    :return: np array
    """
    img_np_array = rgb2gray(np.array(img))
    h, w = img_np_array.shape

    for x in range(0, w):
        for y in range(0, h):
            if img_np_array[y, x] > 0:
                img_np_array[y, x] = 1

    return img_np_array


def create_chromakey_image(img_read, green_low_factor, green_high_factor, saturation, brightness):
    """
    chromakeying method. changes images to hsv and blacks out the given range of colors. The others are left white.
    :param img_read: original image
    :param green_low_factor: low green color filter
    :param green_high_factor: high green color filter
    :param saturation: saturation of the color
    :param brightness: brightness of the color
    :return: binary image
    """
    hsv = rgb2hsv(img_read)

    for pixel_row in hsv:
        for pixel_col in pixel_row:

            if green_low_factor < pixel_col[0] <= green_high_factor \
                    and pixel_col[1] > saturation \
                    and pixel_col[2] > brightness:

                pixel_col[0] = 0
                pixel_col[1] = 0
                pixel_col[2] = 0
            else:

                pixel_col[0] = 1
                pixel_col[1] = 1
                pixel_col[2] = 1

    img_ndarray = np.array(hsv)
    img_rgb = hsv2rgb(img_ndarray)

    img_gray = rgb2gray(img_rgb)
    img_gray_copy = np.copy(img_gray)

    x, y = img_gray_copy.shape

    for i in range(0, x):
        for j in range(0, y):
            pixel = img_gray_copy[i, j]
            if pixel > 0:
                img_gray_copy[i, j] = 1
            else:
                img_gray_copy[i, j] = 0

    return img_gray_copy


