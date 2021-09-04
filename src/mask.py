import cv2
import numpy as np
import os
from tqdm import tqdm


def if_same_rgb(point):
    # 判定rgb值是否相似，true表示检测到的像素为图像阴影或背景
    if point[0] < 110 and point[1] < 110 and point[2] < 110:
        return False
    elif point[0] == point[1]+1 and point[2] == point[1]+2:
        return True
    elif point[0] == point[1] == point[2]:
        return True
    elif point[1] == point[2]-1 or point[1] == point[2]+1 or point[1] == point[2]:
        return True
    return False


def process_mask(img, mask):
    img1 = img.copy()
    # 首先获取原始图像
    img_gray = cv2.cvtColor(mask, cv2.COLOR_BGR2GRAY)  # 转换为灰度图像
    ret, mask = cv2.threshold(img_gray, 127, 255, cv2.THRESH_BINARY)  # 设置阈值，大于175的置为255，小于175的置为0
    mask_inv = cv2.bitwise_not(mask)  # 非运算，mask取反
    img_fg = cv2.bitwise_and(img1, img1, mask=mask_inv)  # 删除了背景区域
    return img_fg


def get_imgs(file_name):
    # 遍历文件夹中的图片，返回字典
    # key为图片文件名，value为numpy格式图片
    project_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    input_dir = os.path.join(project_dir, file_name)
    imgs = {}
    for filename in os.listdir(input_dir):
        # 去除隐藏文件（mac端）
        if filename == ".DS_Store":
            continue
        img = cv2.imread(os.path.join(input_dir, filename))
        imgs[filename] = img
    return imgs


def process_shadow(img):
    # 检测阴影，并将其和背景一起置为灰色
    mask = np.zeros_like(img)
    w = img.shape[0]
    h = img.shape[1]
    for i in tqdm(range(w), desc="Processing Shadow:"):
        for j in range(h):
            point = img[i, j, :]
            # 若该点的rgb值相同或近似相同，则判断为阴影
            if if_same_rgb(point):
                # 阴影全部置为灰色
                mask[i, j, :] = 128
    return mask


def process_bg(input_img):
    # 修改背景颜色为灰色
    img = input_img.copy()
    w = img.shape[0]
    h = img.shape[1]
    for i in tqdm(range(w), desc="Processing Background:"):
        for j in range(h):
            point = img[i, j, :]
            if point[0] == point[1] == point[2] == 0:
                img[i, j, :] = 128
    return img
