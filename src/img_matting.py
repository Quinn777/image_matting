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
    del (img_list[0])
    return img_list


def get_hist(img):
    color = ('b', 'g', 'r')
    plt.subplot(1, 2, 2)
    for i, col in enumerate(color):
        histr = cv2.calcHist([img], [i], None, [256], [0, 256])
        plt.plot(histr, color=col)
        plt.xlim([0, 256])
    plt.show()


def get_contours_area(cnt):
    # 计算countour的面积
    (x, y, w, h) = cv2.boundingRect(cnt)
    return w * h


def waterShed(sourceDir):
    # 读取图片
    img = cv2.imread("../data/10.jpg")
    img = cv2.resize(img, (480, 480))
    # 原图灰度处理,输出单通道图片
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)

    # Step2: 阈值分割，将图像分为黑白两部分
    ret, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

    # Step3: 开运算-先腐蚀再膨胀
    kernel = np.ones((1, 1), np.uint8)
    opening = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel, iterations=4)

    # Step4: 对“开运算”的结果进行膨胀，得到大部分都是背景的区域
    sure_bg = cv2.dilate(opening, kernel, iterations=3)

    # Step5: 通过distanceTransform获取前景区域
    dist_transform = cv2.distanceTransform(opening, cv2.DIST_L2, 5)
    ret, sure_fg = cv2.threshold(dist_transform, 0.2 * dist_transform.max(), 255, 0)

    # Step6: sure_bg与sure_fg相减,得到既有前景又有背景的重合区域
    sure_fg = np.uint8(sure_fg)
    # 此区域和轮廓区域的关系未知
    unknown = cv2.subtract(sure_bg, sure_fg)

    # Step7: 连通区域处理
    # 对连通区域进行标号  序号为 0- N-1
    ret, markers = cv2.connectedComponents(sure_fg, connectivity=8)
    # OpenCV 分水岭算法对物体做的标注必须都 大于1，背景为标号为0,因此对所有markers加1变成了1-N
    markers = markers + 1

    # 去掉属于背景区域的部分（即让其变为0，成为背景）
    # 此语句的Python语法 类似于if ，“unknow==255” 返回的是图像矩阵的真值表。
    # 现在整个markers里面有：0，1，2，3 ..... N
    # 0：代表unknown, 1,2,3,...代表就是连通区域

    markers[unknown == 255] = 0

    # Step8: 分水岭算法
    markers = cv2.watershed(img, markers)  # 分水岭算法后，所有轮廓的像素点被标注为  -1
    # 现在整个markers里面有：-1, 0, 1
    # -1:代表分水岭

    img[markers == -1] = [0, 0, 255]  # 标注为-1 的像素点标红

    # 画图
    plt.subplot(2, 3, 1), plt.imshow(sure_bg, 'gray'), plt.title('background'), plt.xticks([]), plt.yticks([])
    plt.subplot(2, 3, 2), plt.imshow(sure_fg, 'gray'), plt.title('frontground'), plt.xticks([]), plt.yticks([])
    plt.subplot(2, 3, 3), plt.imshow(unknown, 'gray'), plt.title('unknown'), plt.xticks([]), plt.yticks([])
    plt.subplot(2, 3, 4), plt.imshow(markers, 'gray'), plt.title('makers'), plt.xticks([]), plt.yticks([])
    plt.subplot(2, 3, 5), plt.imshow(img), plt.title('img'), plt.xticks([]), plt.yticks([])
    plt.show()
    cv2.imshow("final", img)
    cv2.waitKey(0)

waterShed("data/1.JPG")
