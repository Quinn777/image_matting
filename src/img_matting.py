import cv2
import numpy as np
import os
import matplotlib.pyplot as plt


def get_imgs():
    project_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    input_dir = os.path.join(project_dir, "data")
    img_list = []
    for filename in os.listdir(input_dir):
        img = cv2.imread(os.path.join(input_dir, filename))
        img_list.append(img)
    del(img_list[0])
    return img_list

def get_hist(img):
    color = ('b', 'g', 'r')
    plt.subplot(1, 2, 2)
    for i, col in enumerate(color):
        histr = cv2.calcHist([img], [i], None, [256], [0, 256])
        plt.plot(histr, color=col)
        plt.xlim([0, 256])
    plt.show()

# 读取图片
img_list = get_imgs()
img = img_list[0]
# 缩放
img = cv2.resize(img, (480, 480))
cv2.imshow("ori", img)
# get_hist(img)
# 制作掩膜
mask = cv2.inRange(img, lowerb=(200, 200, 200), upperb=(255, 251, 255))
rows, cols, channels = img.shape

# 腐蚀膨胀
kernel = np.ones((2, 2), np.uint8)
mask = cv2.erode(mask, kernel, iterations=1)
mask = cv2.dilate(mask, kernel, iterations=1)
plt.imshow(mask, cmap='gray')

_, contours, hierarchy = cv2.findContours(image=mask, mode=cv2.RETR_EXTERNAL, method=cv2.CHAIN_APPROX_SIMPLE)


def contours_area(cnt):
    # 计算countour的面积
    (x, y, w, h) = cv2.boundingRect(cnt)
    return w * h

# 获取面积最大的contour
max_cnt = max(contours, key=lambda cnt: contours_area(cnt))
# 创建空白画布
final_mask = np.zeros_like(mask)
# 获取面积最大的 contours
final_mask = cv2.drawContours(final_mask, [max_cnt],0,255,-1)
# 打印罩层
plt.imshow(final_mask, cmap='gray')

# 遍历替换
for i in range(rows):
    for j in range(cols):
        if dilate[i, j] == 255:
            img[i, j] = (0, 0, 255)  # 此处替换颜色，为BGR通道
cv2.imshow('output', img)

cv2.waitKey(0)
