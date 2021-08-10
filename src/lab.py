import numpy as np
import cv2
import matplotlib.pyplot as plt

# read an image with shadow...
# and it converts to BGR color space automatically
def shadow_remove(or_img):
    # covert the BGR image to an YCbCr image
    y_cb_cr_img = cv2.cvtColor(or_img, cv2.COLOR_BGR2YCrCb)

    # copy the image to create a binary mask later
    binary_mask = np.copy(y_cb_cr_img)

    # get mean value of the pixels in Y plane
    y_mean = np.mean(cv2.split(y_cb_cr_img)[0])

    # get standard deviation of channel in Y plane
    y_std = np.std(cv2.split(y_cb_cr_img)[0])

    # classify pixels as shadow and non-shadow pixels
    for i in range(y_cb_cr_img.shape[0]):
        print(f"1-{i}")
        for j in range(y_cb_cr_img.shape[1]):

            if y_cb_cr_img[i, j, 0] < y_mean - (y_std / 3):
                # paint it white (shadow)
                binary_mask[i, j] = [255, 255, 255]
            else:
                # paint it black (non-shadow)
                binary_mask[i, j] = [0, 0, 0]

    # Using morphological operation
    # The misclassified pixels are
    # removed using dilation followed by erosion.
    kernel = np.ones((3, 3), np.uint8)
    erosion = cv2.erode(binary_mask, kernel, iterations=1)

    # sum of pixel intensities in the lit areas
    spi_la = 0

    # sum of pixel intensities in the shadow
    spi_s = 0

    # number of pixels in the lit areas
    n_la = 0

    # number of pixels in the shadow
    n_s = 0

    # get sum of pixel intensities in the lit areas
    # and sum of pixel intensities in the shadow
    for i in range(y_cb_cr_img.shape[0]):
        print(f"2-{i}")
        for j in range(y_cb_cr_img.shape[1]):
            if erosion[i, j, 0] == 0 and erosion[i, j, 1] == 0 and erosion[i, j, 2] == 0:
                spi_la = spi_la + y_cb_cr_img[i, j, 0]
                n_la += 1
            else:
                spi_s = spi_s + y_cb_cr_img[i, j, 0]
                n_s += 1

    # get the average pixel intensities in the lit areas
    average_ld = spi_la / n_la

    # get the average pixel intensities in the shadow
    average_le = spi_s / n_s

    # difference of the pixel intensities in the shadow and lit areas
    i_diff = average_ld - average_le

    # get the ratio between average shadow pixels and average lit pixels
    ratio_as_al = average_ld / average_le

    # added these difference
    for i in range(y_cb_cr_img.shape[0]):
        print(f"3-{i}")
        for j in range(y_cb_cr_img.shape[1]):
            if erosion[i, j, 0] == 255 and erosion[i, j, 1] == 255 and erosion[i, j, 2] == 255:

                y_cb_cr_img[i, j] = [y_cb_cr_img[i, j, 0] + i_diff, y_cb_cr_img[i, j, 1] + ratio_as_al,
                                     y_cb_cr_img[i, j, 2] + ratio_as_al]

    # covert the YCbCr image to the BGR image
    final_image = cv2.cvtColor(y_cb_cr_img, cv2.COLOR_YCR_CB2BGR)


    plt.figure(figsize=(12, 8))
    plt.subplot(1, 2, 1)
    plt.imshow(or_img)
    plt.subplot(1, 2, 2)
    plt.imshow(final_image)
    plt.show()
    return final_image
if __name__ == '__main__':

    import os
    def get_imgs():
        project_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
        input_dir = os.path.join(project_dir, "data")
        img_list = []
        for filename in os.listdir(input_dir):
            img = cv2.imread(os.path.join(input_dir, filename))
            img_list.append(img)
        del (img_list[0])
        return img_list

    # img_list = get_imgs()
    # num = 1
    # for img in img_list:
    #     final_img = shadow_remove(img)
    #     cv2.imwrite(f"../lab_test/{num}.jpg", final_img)
    #     num += 1
    img = cv2.imread("../masked/12.jpg")
    final = shadow_remove(img)
    cv2.imshow("final", cv2.resize(final, (800, 600)))
    cv2.waitKey(0)