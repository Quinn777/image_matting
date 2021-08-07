# -*- coding: utf-8 -*-
'''
    可视化颜色阈值调参软件
'''

import cv2
import numpy as np
import sys

# 更新MASK图像，并且刷新windows
def updateMask():
    global img
    global lowerb
    global upperb
    global mask
    # 计算MASK
    mask = cv2.inRange(img_hsv, lowerb, upperb)

    cv2.imshow('mask', mask)

# 更新阈值
def updateThreshold(x):

    global lowerb
    global upperb

    minH = cv2.getTrackbarPos('minH','image')
    maxH = cv2.getTrackbarPos('maxH','image')
    minS = cv2.getTrackbarPos('minS','image')
    maxS = cv2.getTrackbarPos('maxS', 'image')
    minV = cv2.getTrackbarPos('minV', 'image')
    maxV = cv2.getTrackbarPos('maxV', 'image')

    lowerb = np.int32([minH, minS, minV])
    upperb = np.int32([maxH, maxS, maxV])

    print('更新阈值')
    print(lowerb)
    print(upperb)
    updateMask()

def main(img):
    global img_hsv
    global upperb
    global lowerb
    global mask
    # 将图片转换为HSV格式
    img_hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    # 颜色阈值 Upper
    upperb = None
    # 颜色阈值 Lower
    lowerb = None

    mask = None

    cv2.namedWindow('image', flags= cv2.WINDOW_NORMAL | cv2.WINDOW_FREERATIO)
    # cv2.namedWindow('image')
    cv2.imshow('image', img)

    # cv2.namedWindow('mask')
    cv2.namedWindow('mask', flags= cv2.WINDOW_NORMAL | cv2.WINDOW_FREERATIO)

    # 红色阈值 Bar
    ## 红色阈值下界
    cv2.createTrackbar('minH','image',0,255,updateThreshold)
    ## 红色阈值上界
    cv2.createTrackbar('maxH','image',0,255,updateThreshold)
    ## 设定红色阈值上界滑条的值为255
    cv2.setTrackbarPos('maxH', 'image', 255)
    cv2.setTrackbarPos('minH', 'image', 0)
    # 绿色阈值 Bar
    cv2.createTrackbar('minS','image',0,255,updateThreshold)
    cv2.createTrackbar('maxS','image',0,255,updateThreshold)
    cv2.setTrackbarPos('maxS', 'image', 255)
    cv2.setTrackbarPos('minS', 'image', 0)
    # 蓝色阈值 Bar
    cv2.createTrackbar('minV','image',0,255,updateThreshold)
    cv2.createTrackbar('maxV','image',0,255,updateThreshold)
    cv2.setTrackbarPos('maxV', 'image', 255)
    cv2.setTrackbarPos('minV', 'image', 0)

    # 首次初始化窗口的色块
    # 后面的更新 都是由getTrackbarPos产生变化而触发
    updateThreshold(None)

    print("调试棋子的颜色阈值, 键盘摁e退出程序")
    while cv2.waitKey(0) != ord('e'):
        continue

    cv2.destroyAllWindows()
    return mask

if __name__ == "__main__":
    # 样例图片 (从命令行中填入)

    img = cv2.imread("tmp_bin.png")
    # img = cv2.resize(img, (1000, 800))

    # mask = main(img)
    # cv2.imwrite(f'../mask/{img_name}', mask)
    # from img_matting import *
    # waterShed(img)
    img = cv2.bilateralFilter(img, 10, 200, 200) # 双边滤波

    bgr = cv2.cvtColor(img, cv2.COLOR_HSV2BGR)
    gray = cv2.cvtColor(bgr, cv2.COLOR_BGR2GRAY)

    ret, binary = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)

    # 轮廓检测
    _, contours, hierarchy = cv2.findContours(binary, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)

    # 新打开一个图片，我这里这张图片是一张纯白图片
    newImg = np.ones([800, 1000, 3], dtype=np.uint8) * 255
    # 画图
    cv2.drawContours(newImg, contours, -1, (0, 0, 0), -1, cv2.LINE_AA)

    w = newImg.shape[0]
    h = newImg.shape[1]
    channels = newImg.shape[2]

    mask = np.zeros((w + 2, h + 2), np.uint8)

    cv2.floodFill(newImg, mask, (0, 0), (100, 100, 100), (1, 1, 1), (1, 1, 1), 4)
    from PIL import Image

    for row in range(h):  # 遍历每一行
        for col in range(w):  # 遍历每一列
            for channel in range(channels):  # 遍历每个通道（三个通道分别是BGR）
                if newImg[col][row][channel] == 0:
                    newImg[col][row][channel] = 255
                elif newImg[col][row][channel] == 100:
                    newImg[col][row][channel] = 0
    mask = newImg
                    # 展示
    cv2.imshow("img", mask)
    cv2.waitKey(0)

    img_name = "12.jpg"
    img = cv2.imread(f"../lab_test/{img_name}")
    img = cv2.resize(img, (1000, 800))
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    mask = cv2.cvtColor(mask, cv2.COLOR_BGR2GRAY)

    mask = cv2.GaussianBlur(mask, (3, 3), 0)

    img_fg = cv2.bitwise_and(gray, gray, mask=mask)
    cv2.imshow("img", img_fg)
    cv2.waitKey(0)



