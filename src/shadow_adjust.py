import os
import sys
import cv2
import numpy as np


class PSShadowHighlight:
    """
    色阶调整
    """

    def __init__(self, image):
        self.shadows_light = 50

        img = image.astype(np.float) / 255.0

        srcR = img[:, :, 2]
        srcG = img[:, :, 1]
        srcB = img[:, :, 0]
        srcGray = 0.299 * srcR + 0.587 * srcG + 0.114 * srcB

        # 高光选区
        # luminance = luminance * luminance
        # luminance = np.where(luminance > 0.64, luminance, 0)

        # 阴影选区
        luminance = (1 - srcGray) * (1 - srcGray)

        self.maskThreshold = np.mean(luminance)
        mask = luminance > self.maskThreshold

        imgRow = np.size(img, 0)
        imgCol = np.size(img, 1)
        print("imgRow:%d, imgCol:%d, maskThreshold:%f" % (imgRow, imgCol, self.maskThreshold))
        print("shape:", img.shape)

        self.rgbMask = np.zeros([imgRow, imgCol, 3], dtype=bool)
        self.rgbMask[:, :, 0] = self.rgbMask[:, :, 1] = self.rgbMask[:, :, 2] = mask

        self.rgbLuminance = np.zeros([imgRow, imgCol, 3], dtype=float)
        self.rgbLuminance[:, :, 0] = self.rgbLuminance[:, :, 1] = self.rgbLuminance[:, :, 2] = luminance

        self.midtonesRate = np.zeros([imgRow, imgCol, 3], dtype=float)
        self.brightnessRate = np.zeros([imgRow, imgCol, 3], dtype=float)

    def adjust_image(self, img):
        maxRate = 4
        brightness = (self.shadows_light / 100.0 - 0.0001) / maxRate
        midtones = 1 + maxRate * brightness

        self.midtonesRate[self.rgbMask] = midtones
        self.midtonesRate[~self.rgbMask] = (midtones - 1.0) / self.maskThreshold * self.rgbLuminance[
            ~self.rgbMask] + 1.0

        self.brightnessRate[self.rgbMask] = brightness
        self.brightnessRate[~self.rgbMask] = (1 / self.maskThreshold * self.rgbLuminance[~self.rgbMask]) * brightness

        outImg = 255 * np.power(img / 255.0, 1.0 / self.midtonesRate) * (1.0 / (1 - self.brightnessRate))

        img = outImg
        img[img < 0] = 0
        img[img > 255] = 255

        img = img.astype(np.uint8)
        return img


def ps_shadow_highlight_adjust_and_save_img(psSH, origin_image):
    psSH.shadows_light = 50
    image = psSH.adjust_image(origin_image)
    cv2.imwrite('py_sh_out_01.png', image)


def ps_shadow_highlight_adjust(origin_image):
    """
    阴影提亮调整
    """
    psSH = PSShadowHighlight(origin_image)

    # ps_shadow_highlight_adjust_and_save_img(psSH, origin_image)

    def update_shadows_light(x):
        psSH.shadows_light = x

    # 创建图片显示窗口
    title = "ShadowHighlight"
    cv2.namedWindow(title, cv2.WINDOW_NORMAL)
    cv2.resizeWindow(title, 800, 600)
    cv2.moveWindow(title, 0, 0)

    # 创建阴影提亮操作窗口
    option_title = "Option"
    cv2.namedWindow(option_title, cv2.WINDOW_NORMAL)
    cv2.resizeWindow(option_title, 400, 20)
    cv2.moveWindow(option_title, 0, 630)
    cv2.createTrackbar('shadows_light', option_title, psSH.shadows_light, 100, update_shadows_light)

    while True:
        image = psSH.adjust_image(origin_image)
        cv2.imshow(title, image)
        if cv2.waitKey(1) == ord('q'):
            break
    cv2.destroyAllWindows()
    return image


if __name__ == '__main__':
    '''
        运行环境：Python 3
        执行：python3 ps_shadow_hightlight.py <图片路径>
        如：python3 ps_shadow_hightlight.py test.jpg
    '''
    img_path = "../data/10.jpg"
    print("img_path Params:", img_path)
    img = cv2.imread(img_path)
    img = cv2.resize(img, (500, 500))
    final_img = ps_shadow_highlight_adjust(img)