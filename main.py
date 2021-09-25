from src.mask import *
import matplotlib.pyplot as plt
import time
if __name__ == '__main__':
    img_dict = get_imgs("data")
    for img_name, first_img in img_dict.items():
        print(f"Processing {img_name}...")
        begin = time.time()
        # 去除阴影，生成掩膜
        second_img = process_shadow(first_img)
        # 消去白色噪点
        # 核函数尺寸，取值范围3-27之间的奇数，默认为3；建议取值3、5、7过大图像模糊化严重，运算慢
        k_size = 11
        third_img = cv2.medianBlur(second_img, ksize=k_size)
        # third_img = cv2.fastNlMeansDenoisingColored(second_img, None, 14, 12, 7, 21)
        # 缩放
        se = cv2.resize(second_img, (500, 500))
        cv2.imshow("ori", se)
        tri = cv2.resize(third_img, (500, 500))
        cv2.imshow("final", tri)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
        # 根据掩膜过滤背景
        forth_img = process_mask(first_img, third_img)
        # 将黑色背景转为灰色
        out = process_bg(forth_img)

        end = time.time()
        during_time = end-begin

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
        print(f"{img_name} written successfully! Time:{during_time}")