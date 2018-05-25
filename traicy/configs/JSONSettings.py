__name__ = "JSONSettings Parser"

from enum import Enum
import json
import codecs

__imported__ = False

__i_dim__ = 0
__i_dim_s__ = 0
__i_border__ = 0

__f_canny__ = 0.0
__f_bin_gauss__ = 0.0
__f_bin_thresh__ = 0.0

__f_green_low__ = 0.0
__f_green_high__ = 0.0

__f_green_saturation__ = 0.0
__f_green_brightness__ = 0.0

__l_possible_filename = list()
__f_contours_length__ = 0.0

__f_fill_out_length__ = 0.0
__f_chunk_border_strength__ = 0.0

__data__ = {}


class JSONValues (Enum):
    IMAGE_DIMENSION = 0
    IMAGE_DIMENSION_SMALL = 1
    IMAGE_BORDER = 2

    FILTER_CANNY = 3
    FILTER_BIN_GAUSS = 4
    FILTER_BIN_THRESHOLD = 5

    FILTER_GREEN_LOW = 6
    FILTER_GREEN_HIGH = 7

    FILTER_GREEN_SATURATION = 8
    FILTER_GREEN_BRIGHTNESS = 9

    LOADING_POSSIBLE_FILENAME = 10
    FILTER_CONTOURS_LENGTH = 11

    FILTER_FILL_OUT_LENGTH = 12
    FILTER_CHUNK_BORDER_STRENGTH = 13


def parse_data(filename):
    with open(filename, encoding='utf-8') as data_file:

        data = json.loads(data_file.read())        

        # Change variable access to global
        global __data__
        __data__ = data

        if data is not None:

            # Change variable access to global
            global __i_dim__, __i_dim_s__, __i_border__
            global __f_canny__, __f_bin_gauss__, __f_bin_thresh__, __f_green_low__, __f_green_high__, \
                __f_green_saturation__, __f_green_brightness__
            global __l_possible_filename
            global __f_contours_length__, __f_fill_out_length__, __f_chunk_border_strength__
            global __imported__

            image_access = data['image']
            filter_access = data['filter']
            loading_access = data['loading']

            if image_access is not None:
                __i_dim__ = image_access['dimension']
                __i_dim_s__ = image_access['dimension_small']
                __i_border__ = image_access['border']

            if filter_access is not None:
                __f_canny__ = filter_access['canny']
                __f_bin_gauss__ = filter_access['binary_gauss']
                __f_bin_thresh__ = filter_access['binary_threshold']

                __f_green_low__ = filter_access['green_low']
                __f_green_high__ = filter_access['green_high']

                __f_green_saturation__ = filter_access['green_saturation']
                __f_green_brightness__ = filter_access['green_brightness']

                __f_contours_length__ = filter_access['contours_length']

            if loading_access is not None:
                __l_possible_filename = loading_access['possible_filename']

            __f_fill_out_length__ = filter_access['schmiering']
            __f_chunk_border_strength__ = filter_access['chunk_border']

            __imported__ = True

    data_file.close()


def get_data(json_value, *filename):
    if __imported__:

        if json_value == JSONValues.IMAGE_DIMENSION:
            return __i_dim__
        if json_value == JSONValues.IMAGE_DIMENSION_SMALL:
            return __i_dim_s__
        if json_value == JSONValues.IMAGE_BORDER:
            return __i_border__

        if json_value == JSONValues.FILTER_CANNY:
            return __f_canny__
        if json_value == JSONValues.FILTER_BIN_GAUSS:
            return __f_bin_gauss__
        if json_value == JSONValues.FILTER_BIN_THRESHOLD:
            return __f_bin_thresh__
        if json_value == JSONValues.FILTER_GREEN_LOW:
            return __f_green_low__
        if json_value == JSONValues.FILTER_GREEN_HIGH:
            return __f_green_high__
        if json_value == JSONValues.FILTER_GREEN_SATURATION:
            return __f_green_saturation__
        if json_value == JSONValues.FILTER_GREEN_BRIGHTNESS:
            return __f_green_brightness__

        if json_value == JSONValues.FILTER_CONTOURS_LENGTH:
            return __f_contours_length__
        if json_value == JSONValues.FILTER_FILL_OUT_LENGTH:
            return __f_fill_out_length__
        if json_value == JSONValues.FILTER_CHUNK_BORDER_STRENGTH:
            return __f_chunk_border_strength__

        if json_value == JSONValues.LOADING_POSSIBLE_FILENAME:
            return __l_possible_filename
    else:
        if filename is not None or filename != "":
            parse_data(filename)
            return get_data(json_value)
        else:
            return "NO DATA FOUND"


def write_data(filename, json_value, value):
    if not __imported__:
        parse_data(filename)

    global __i_dim__, __i_dim_s__, __i_border__
    global __f_canny__, __f_bin_gauss__, __f_bin_thresh__, __f_green_low__, __f_green_high__, \
        __f_green_saturation__, __f_green_brightness__
    global __l_possible_filename
    global __f_contours_length__, __f_fill_out_length__, __f_chunk_border_strength__

    if json_value == JSONValues.IMAGE_DIMENSION:
        __data__['image']['dimension'] = value
        __i_dim__ = value

    if json_value == JSONValues.IMAGE_DIMENSION_SMALL:
        __data__['image']['dimension_small'] = value
        __i_dim_s__ = value

    if json_value == JSONValues.IMAGE_BORDER:
        __data__['image']['border'] = value
        __i_border__ = value

    ##################################################

    if json_value == JSONValues.FILTER_CANNY:
        __data__['filter']['canny'] = value
        __f_canny__ = value

    if json_value == JSONValues.FILTER_BIN_GAUSS:
        __data__['filter']['binary_gauss'] = value
        __f_bin_gauss__ = value

    if json_value == JSONValues.FILTER_BIN_THRESHOLD:
        __data__['filter']['binary_threshold'] = value
        __f_bin_thresh__ = value

    ##################################################

    if json_value == JSONValues.FILTER_BIN_THRESHOLD:
        __data__['filter']['green_low'] = value
        __f_green_low__ = value

    if json_value == JSONValues.FILTER_BIN_THRESHOLD:
        __data__['filter']['green_high'] = value
        __f_green_high__ = value

    if json_value == JSONValues.FILTER_BIN_THRESHOLD:
        __data__['filter']['green_saturation'] = value
        __f_green_saturation__ = value

    if json_value == JSONValues.FILTER_BIN_THRESHOLD:
        __data__['filter']['green_brightness'] = value
        __f_green_brightness__ = value

    ##################################################

    if json_value == JSONValues.LOADING_POSSIBLE_FILENAME:
        __data__['loading']['possible_filename'] = value
        __l_possible_filename = value

    ##################################################

    if json_value == JSONValues.FILTER_CONTOURS_LENGTH:
        __data__['filter']['contours_length'] = value
        __f_contours_length__ = value

    ##################################################

    if json_value == JSONValues.FILTER_FILL_OUT_LENGTH:
        __data__['filter']['schmiering'] = value
        __f_contours_length__ = value

    if json_value == JSONValues.FILTER_CHUNK_BORDER_STRENGTH:
        __data__['filter']['chunk_border'] = value
        __f_contours_length__ = value

    with open(filename, 'wb') as outfile:
        json.dump(__data__, codecs.getwriter('utf-8')(outfile), indent=4, ensure_ascii=False)
        outfile.flush()
        outfile.close()
