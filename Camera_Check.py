import numpy as np
import time
import argparse
import json

"""Get image paths from arguments"""


def get_image_arguments():
    image_paths = []
    parser = argparse.ArgumentParser()
    parser.add_argument('image_list', nargs='*')
    args = parser.parse_args()
    image_paths = args.image_list
    return image_paths


"""Create and define the return dictionary """


def create_return_dict():
    ret_dict = {}
    ret_dict['Error'] = ''
    ret_dict['nr_of_images'] = 0
    ret_dict['image_list'] = []
    return ret_dict


"""Image check function"""


def image_check(image_path_list, ret_dict):
    ret_dict['nr_of_images'] = len(image_path_list)
    ret_dict['image_list'] = []  # image_path_list


if __name__ == '__main__':
    """Create the return dictionary"""
    return_dict = create_return_dict()

    """Get the image list from arguments"""
    image_list = get_image_arguments()

    image_check(image_list, return_dict)

    #return_dict['image_list'] = image_list
    #return_dict['nr_of_images'] = len(image_list)

    print json.dumps(return_dict)
