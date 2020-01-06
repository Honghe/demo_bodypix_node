# -*- coding: utf-8 -*-

import cv2
import json
import numpy as np
from matplotlib import pyplot as plt

rainbow = [
    [110, 64, 170], [143, 61, 178], [178, 60, 178], [210, 62, 167],
    [238, 67, 149], [255, 78, 125], [255, 94, 99], [255, 115, 75],
    [255, 140, 56], [239, 167, 47], [217, 194, 49], [194, 219, 64],
    [175, 240, 91], [135, 245, 87], [96, 247, 96], [64, 243, 115],
    [40, 234, 141], [28, 219, 169], [26, 199, 194], [33, 176, 213],
    [47, 150, 224], [65, 125, 224], [84, 101, 214], [99, 81, 195]
]

background = [255, 255, 255]
opacity = 0.3


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


if __name__ == '__main__':
    fig = plt.figure(figsize=(12, 4))
    img = load_image('../images/kids.jpg')
    partSegmentation = load_partSegmentation('../output/segs.json')
    coloredPartImage = toColoredPartMask(partSegmentation, img=img)
    mask_img = drawMask(img, coloredPartImage, opacity)

    # plot
    images = [img, coloredPartImage, mask_img]
    rows = 1
    columns = 3
    for i in range(len(images)):
        fig.add_subplot(rows, columns, i + 1)
        plt.imshow(images[i])
    plt.show()
