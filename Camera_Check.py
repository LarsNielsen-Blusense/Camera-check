import numpy as np
import time
import argparse
import json
from PIL import Image
import cv2
import os

__version__ = 0.1


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
    ret_dict['B_G_R_values'] = []
    ret_dict['B_G_R_background_values'] = []
    ret_dict['Image_size'] = []
    ret_dict['Camera_QC_passed'] = False
    ret_dict['Background_Image'] = ''
    ret_dict['Version'] = __version__
    return ret_dict


"""Image check function"""


def image_check(image_path_list, ret_dict):
    ret_dict['nr_of_images'] = len(image_path_list)
    ret_dict['image_list'] = image_path_list
    if len(image_path_list) > 0:
        background = image_path_list[0].replace('11.jpg', '10.jpg')
        ret_dict['Background_Image'] = background
        if os.path.isfile(background):
            for item in image_path_list:
                if os.path.isfile(item):
                    im = cv2.imread(item)
                    ret_dict['Image_size'].append([im.shape[0], im.shape[1]])
                    B_G_R_values = [np.average(im[0:479, 170:300, 0]), np.average(im[0:479, 170:300, 1]), np.average(im[0:479, 170:300, 2])]
                    ret_dict['B_G_R_values'].append(B_G_R_values)
                else:
                    ret_dict['Error'] = ret_dict['Error'] + item + ' does not exits\n'
        else:
            ret_dict['Error'] = ret_dict['Error'] + background + ' does not exits\n'
    else:
        ret_dict['Error'] = 'Not 3 Images supplied'
        return
    if ret_dict['Error'] == '':
        QC_sum = 0
        im_nr = 0
        for item in ret_dict['B_G_R_values']:
            im_background = cv2.imread(background)
            ret_dict['B_G_R_background_values'] = [np.average(im_background[0:479, 170:300, 0]), np.average(
                im_background[0:479, 170:300, 1]), np.average(im_background[0:479, 170:300, 2])]
            if item[im_nr] > ret_dict['B_G_R_background_values'][im_nr] * 100:
                QC_sum += 1
                im_nr += 1
        if QC_sum == len(ret_dict['B_G_R_values']):
            ret_dict['Camera_QC_passed'] = True


def delete_images(ret_dict):
    if os.path.isfile(ret_dict['Background_Image']):
        os.remove(ret_dict['Background_Image'])
    for item in ret_dict['image_list']:
        if os.path.isfile(item):
            os.remove(item)


if __name__ == '__main__':
    """Create the return dictionary"""
    return_dict = create_return_dict()

    """Get the image list from arguments"""
    image_list = get_image_arguments()

    """Check images taken by camera"""
    image_check(image_list, return_dict)

    """Print return dictionary"""
    print json.dumps(return_dict)

    """Delete the pictures take"""
    delete_images(return_dict)
