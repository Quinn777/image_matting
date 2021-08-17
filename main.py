from src.mask import *

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