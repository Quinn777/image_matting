import cv2
import numpy as np
from matplotlib import pyplot as plt
import os
from tqdm import tqdm


def if_same_rgb(point):
    if point[0] < 110 and point[1] < 110 and point[2] < 110:
        return False
    elif point[0] == point[1]+1 and point[2] == point[1]+2:
        return True
    elif point[0] == point[1] == point[2]:
        return True
    elif point[1] == point[2]-1 or point[1] == point[2]+1 or point[1] == point[2]:
        return True
    return False


def mask_process(img, measure, mask):
    img1 = img.copy()
    # I want to put logo on top-left corner, So I create a ROI
    # 首先获取原始图像roi
    rows, cols, channels = img1.shape  # 获取图像2的属性
    roi = img1[0:rows, 0:cols]  # 选择roi范围

    img2gray = cv2.cvtColor(mask, cv2.COLOR_BGR2GRAY)  # 转换为灰度图像
    ret, mask = cv2.threshold(img2gray, 127, 255, cv2.THRESH_BINARY)  # 设置阈值，大于175的置为255，小于175的置为0
    mask_inv = cv2.bitwise_not(mask)  # 非运算，mask取反

    img1_bg = cv2.bitwise_and(roi, roi, mask=mask)  # 删除了ROI中的logo区域
    img2_fg = cv2.bitwise_and(img1, img1, mask=mask_inv)  # 删除了logo中的空白区域

    dst = cv2.add(img1_bg, img2_fg)
    img1[0:rows, 0:cols] = dst


    # plt.subplot(2, 2, 1)
    # plt.imshow(mask)
    #
    # plt.subplot(2, 2, 2)
    # plt.imshow(img1_bg)
    # # plt.show()
    # plt.subplot(2, 2, 3)
    # plt.imshow(img2_fg)
    # # plt.show()
    # plt.subplot(2, 2, 4)
    # plt.imshow(dst)
    # plt.show()
    return img2_fg


def get_imgs(file_name):
    project_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    input_dir = os.path.join(project_dir, file_name)
    img_dict = {}
    for filename in os.listdir(input_dir):
        if filename == ".DS_Store":
            continue
        img = cv2.imread(os.path.join(input_dir, filename))
        img_dict[filename] = img
    return img_dict


def process_shadow(img):
    final = np.zeros_like(img)
    w = img.shape[0]
    h = img.shape[1]
    for i in tqdm(range(w)):
        for j in range(h):
            point = img[i, j, :]
            if if_same_rgb(point):
                final[i, j, :] = 128
    # plt.subplot(1, 2, 1)
    # plt.imshow(img)
    # plt.subplot(1, 2, 2)
    # plt.imshow(final)
    # plt.show()
    return final


def process_bg(img):
    w = img.shape[0]
    h = img.shape[1]
    for i in tqdm(range(w)):
        for j in range(h):
            point = img[i, j, :]
            if point[0] == point[1] == point[2] == 0:
                img[i, j, :] = 128
    # plt.subplot(1, 2, 1)
    # plt.imshow(img)
    # plt.subplot(1, 2, 2)
    # plt.imshow(final)
    # plt.show()
    return img

if __name__ == '__main__':
    img_dict = get_imgs("data")
    for img_name, first_img in img_dict.items():

        second_img = process_shadow(first_img)
        # final = mask_process(img, cv2.THRESH_OTSU)
        Ksize = 9  # 核函数尺寸，取值范围3-27之间的奇数，默认为3；建议取值3、5、7过大图像模糊化严重，运算慢
        third_img = cv2.medianBlur(second_img, ksize=Ksize)
        # plt.subplot(1, 2, 1)
        # plt.imshow(img)
        # plt.subplot(1, 2, 2)
        # plt.imshow(out)
        # plt.show()
        forth_img = mask_process(first_img, cv2.THRESH_TRIANGLE, third_img)
        out = process_bg(forth_img)
        cv2.imwrite(f"../output/{img_name}", out)
        print(f"{img_name} written successfully!")
    # img_dict = get_imgs("mask")
    # for img_name, img in img_dict.items():w
    #     dst = cv2.fastNlMeansDenoisingColored(img, None, 15, 10, 7, 21)
    #     plt.subplot(121), plt.imshow(img)
    #     plt.subplot(122), plt.imshow(dst)
    #     plt.show()

