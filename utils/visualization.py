# -*- coding: utf-8 -*-
import json
import logging
import os
import sys

import cv2
import numpy as np

rainbow = [
    [110, 64, 170], [143, 61, 178], [178, 60, 178], [210, 62, 167],
    [238, 67, 149], [255, 78, 125], [255, 94, 99], [255, 115, 75],
    [255, 140, 56], [239, 167, 47], [217, 194, 49], [194, 219, 64],
    [175, 240, 91], [135, 245, 87], [96, 247, 96], [64, 243, 115],
    [40, 234, 141], [28, 219, 169], [26, 199, 194], [33, 176, 213],
    [47, 150, 224], [65, 125, 224], [84, 101, 214], [99, 81, 195]
]

background = [255, 255, 255]
opacity = 0.05


def load_image(file_path):
    img = cv2.imread(file_path)
    # bgr to rgb
    img = img[:, :, ::-1]
    return img


def load_partSegmentation(file_path):
    return json.load(open(file_path))


def toColoredPartMask(partSegmentation, img, partColors=rainbow):
    """
    for segmentPersonParts
    :param partSegmentation:
    :param partColors:
    :return:
    """
    data = partSegmentation['data']
    img_list = [partColors[data[i]] if data[i] >= 0 else background for i in data]
    img_np = np.array(img_list).reshape(img.shape)
    return img_np


def drawMask(img, coloredPartImage, opacity):
    img1 = img
    img2 = coloredPartImage
    alpha = opacity
    out_img = np.zeros(img1.shape, dtype=img1.dtype)
    out_img[:, :, :] = (alpha * img1[:, :, :]) + ((1 - alpha) * img2[:, :, :])
    return out_img


def walk_dir_for_segmentation(root_dir):
    img_dir = os.path.join(root_dir, 'jpgs')
    json_dir = os.path.join(root_dir, 'jsons')
    masked_jpgs_dir = os.path.join(root_dir, 'masked_jpgs')
    for img_file in os.listdir(img_dir):
        print('preprocess file: {}'.format(img_file))
        img_path = os.path.join(img_dir, img_file)
        img = load_image(img_path)
        json_path = os.path.join(json_dir, img_file.split('.')[0] + '.json')
        partSegmentation = load_partSegmentation(json_path)
        coloredPartImage = toColoredPartMask(partSegmentation, img=img)
        mask_img = drawMask(img, coloredPartImage, opacity)
        # save image
        img_basename = os.path.basename(img_path)
        output_img_path = os.path.join(masked_jpgs_dir, img_basename)
        os.makedirs(masked_jpgs_dir, exist_ok=True)
        cv2.imwrite(output_img_path, mask_img[:, :, ::-1])


if __name__ == '__main__':
    # for dir
    if len(sys.argv) <= 1:
        logging.error('Need run with: {} <dir>'.format(os.path.basename(sys.argv[0])))
    else:
        root_dir = os.path.abspath(sys.argv[1])
        walk_dir_for_segmentation(root_dir)

    # for one jpg
    # img_path = '../images/kids.jpg'
    # json_path = '../output/kids.json'
    # output_dir = '../masked_jpg'
    # img = load_image(img_path)
    # partSegmentation = load_partSegmentation(json_path)
    # coloredPartImage = toColoredPartMask(partSegmentation, img=img)
    # mask_img = drawMask(img, coloredPartImage, opacity)
    # from matplotlib import pyplot as plt
    # fig = plt.figure(figsize=(12, 4))
    # images = [img, coloredPartImage, mask_img]
    # rows = 1
    # columns = 3
    # for i in range(len(images)):
    #     fig.add_subplot(rows, columns, i + 1)
    #     plt.imshow(images[i])
    # plt.show()
