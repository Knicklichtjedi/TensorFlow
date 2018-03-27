__name__ = "JSONSettings Parser"

import json

__i_dim = 0
__i_dim_s = 0
__i_border = 0
__f_canny = 0.0
__f_bin_gauss = 0.0
__f_bin_thresh = 0.0


def parse_data(filename):
    with open(filename, encoding='utf-8') as data_file:
        data = json.loads(data_file.read())

        if data is not None:

            # Change variable access to global
            global i_dim, i_dim_s, i_border, f_canny, f_bin_gauss, f_bin_thresh

            image_access = data['image']
            filter_access = data['filter']

            i_dim = (image_access[0])['dimension']
            i_dim_s = (image_access[1])['dimension_small']
            i_border = (image_access[2])['border']

            f_canny = (filter_access[0])['canny']
            f_bin_gauss = (filter_access[1])['binary_gauss']
            f_bin_thresh = (filter_access[2])['binary_threshold']


def get_dimension():
    return i_dim


def get_dimension_small():
    return i_dim_s


def get_border():
    return i_border


def get_canny():
    return f_canny


def get_binary_gauss():
    return f_bin_gauss


def get_binary_threshold():
    return f_bin_thresh
