import cv2
import numpy as np


def max_filter(image,filter_size):
    # padding操作，在最大滤波中需要在原图像周围填充（filter_size//2）个小的数字，一般取-1
    # 先生成一个全为-1的矩阵，大小和padding后的图像相同
    empty_image = np.full((image.shape[0] + (filter_size // 2) * 2, image.shape[1] + (filter_size // 2) * 2), -1)
    # 将原图像填充进矩阵
    empty_image[(filter_size // 2):empty_image.shape[0] - (filter_size // 2),
    (filter_size // 2):empty_image.shape[1] - (filter_size // 2)] = image.copy()
    # 创建结果矩阵，和原图像大小相同
    result = np.full((image.shape[0], image.shape[1]), -1)

    # 遍历原图像中的每个像素点，对于点，选取其周围（filter_size*filter_size）个像素中的最大值，作为结果矩阵中的对应位置值
    for h in range(filter_size // 2, empty_image.shape[0]-filter_size // 2):
        for w in range(filter_size // 2, empty_image.shape[1]-filter_size // 2):
            filter = empty_image[h - (filter_size // 2):h + (filter_size // 2) + 1,
                     w - (filter_size // 2):w + (filter_size // 2) + 1]
            result[h-filter_size // 2, w-filter_size // 2] = np.amax(filter)
    return result


def min_filter(image,filter_size):
    # padding操作，在最大滤波中需要在原图像周围填充（filter_size//2）个大的数字，一般取大于255的
    # 先生成一个全为-1的矩阵，大小和padding后的图像相同
    empty_image = np.full((image.shape[0] + (filter_size // 2) * 2, image.shape[1] + (filter_size // 2) * 2), 400)
    # 将原图像填充进矩阵
    empty_image[(filter_size // 2):empty_image.shape[0] - (filter_size // 2),
    (filter_size // 2):empty_image.shape[1] - (filter_size // 2)] = image.copy()
    # 创建结果矩阵，和原图像大小相同
    result = np.full((image.shape[0], image.shape[1]), 400)

    # 遍历原图像中的每个像素点，对于点，选取其周围（filter_size*filter_size）个像素中的最小值，作为结果矩阵中的对应位置值
    for h in range(filter_size // 2, empty_image.shape[0]-filter_size // 2):
        for w in range(filter_size // 2, empty_image.shape[1]-filter_size // 2):
            filter = empty_image[h - (filter_size // 2):h + (filter_size // 2) + 1,
                     w - (filter_size // 2):w + (filter_size // 2) + 1]
            result[h-filter_size // 2, w-filter_size // 2] = np.amin(filter)
    return result


def remove_shadow(image_path):
    image = cv2.imread(image_path)
    src_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    max_result=max_filter(src_gray, 30)
    min_result=min_filter(max_result, 30)
    result=src_gray-min_result
    result=cv2.normalize(result, None, 0, 255, norm_type=cv2.NORM_MINMAX)
    return result


if __name__ == '__main__':
    img = cv2.imread("../data/10.jpg")
    final_img = remove_shadow("../data/10.jpg")
    cv2.imshow("ori_img", img)
    cv2.imshow("final_img", final_img)
    cv2.waitKey(0)