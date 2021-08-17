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


def process_mask(img, mask):
    img1 = img.copy()
    # I want to put logo on top-left corner, So I create a ROI
    # 首先获取原始图像roi
    rows, cols, channels = img1.shape  # 获取图像2的属性
    roi = img1[0:rows, 0:cols]  # 选择roi范围

    img2gray = cv2.cvtColor(mask, cv2.COLOR_BGR2GRAY)  # 转换为灰度图像
    ret, mask = cv2.threshold(img2gray, 127, 255, cv2.THRESH_BINARY)  # 设置阈值，大于175的置为255，小于175的置为0
    mask_inv = cv2.bitwise_not(mask)  # 非运算，mask取反

    img1_bg = cv2.bitwise_and(roi, roi, mask=mask)  # 删除了ROI中的前景区域
    img2_fg = cv2.bitwise_and(img1, img1, mask=mask_inv)  # 删除了背景区域

    return img2_fg


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
    final = np.zeros_like(img)
    w = img.shape[0]
    h = img.shape[1]
    for i in tqdm(range(w), desc="Processing Shadow:"):
        for j in range(h):
            point = img[i, j, :]
            # 若该点的rgb值相同或近似相同，则判断为阴影
            if if_same_rgb(point):
                # 阴影全部置为灰色
                final[i, j, :] = 128
    return final


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


if __name__ == '__main__':
    img_dict = get_imgs("data")
    for img_name, first_img in img_dict.items():
        # 去除阴影，生成掩膜
        second_img = process_shadow(first_img)
        # 消去白色噪点
        # 核函数尺寸，取值范围3-27之间的奇数，默认为3；建议取值3、5、7过大图像模糊化严重，运算慢
        k_size = 9
        third_img = cv2.medianBlur(second_img, ksize=k_size)
        # 根据掩膜过滤背景
        forth_img = process_mask(first_img, third_img)
        # 将黑色背景转为灰色
        out = process_bg(forth_img)

        plt.subplot(2, 2, 1)
        plt.imshow(second_img)
        plt.subplot(2, 2, 2)
        plt.imshow(third_img)
        plt.subplot(2, 2, 3)
        plt.imshow(forth_img)
        plt.subplot(2, 2, 4)
        plt.imshow(out)
        plt.show()

        cv2.imwrite(f"../output/{img_name}", out)
        print(f"{img_name} written successfully!")


