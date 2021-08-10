import cv2
import numpy as np
# 读取图片并缩放方便显示
img = cv2.imread('../lab_test/15.jpg')
height, width = img.shape[:2]
size = (int(width * 0.2), int(height * 0.2))
# 缩放
img = cv2.resize(img, size, interpolation=cv2.INTER_AREA)

# BGR转化为HSV
HSV = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)


# 鼠标点击响应事件
def getposHsv(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN:
        print("HSV is", HSV[y, x])



def getposBgr(event, x, y, flags, param):
    w = img.shape[0]
    h = img.shape[1]
    mask = np.zeros((w + 2, h + 2), np.uint8)
    if event == cv2.EVENT_LBUTTONDOWN:
        print("Bgr is", img[y, x])
        # cv2.floodFill(img, mask, (y, x), (255, 255, 255), (2, 2, 3), (4, 4, 3), 4)
        # cv2.imshow("floodfill", img)
        # cv2.waitKey(0)
        # cv2.destroyWindow("floodfill")


cv2.imshow("imageHSV", HSV)
cv2.imshow('image', img)
cv2.setMouseCallback("imageHSV", getposHsv)
cv2.setMouseCallback("image", getposBgr)

cv2.waitKey(0)