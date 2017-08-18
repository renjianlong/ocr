# _*_ coding:utf-8_*_
import sys
from PIL import Image
from PIL import ImageFilter
from PIL import ImageEnhance

"""
binary:图片增强:二值化处理
:img：待处理图片
：threshold:阈值设定
"""


def binary(img, threshold):
    pixdata = img.load()
    w, h = img.size
    for j in range(h):
        for i in range(w):
            if pixdata[i, j] < threshold:
                pixdata[i, j] = 0
            else:
                pixdata[i, j] = 255
    return img


"""
denoisy:图片去噪
        像素值>245的领域像素,判别为背景色
        一个像素上下左右四个像素有超过两个属于背景色，该像素就是目标点，否则就是噪声
img:待处理图片
"""


def denoisy(img):
    pixdata = img.load()
    w, h = img.size
    for j in range(1, h - 1):
        for i in range(1, w - 1):
            count = 0
            if pixdata[i, j - 1] > 245:
                count += 1
            if pixdata[i, j + 1] > 245:
                count += 1
            if pixdata[i - 1, j] > 245:
                count += 1
            if pixdata[i + 1, j] > 245:
                count += 1
            if count > 2:
                pixdata[i, j] = 255
    return img


"""
img_transfer():图片转化，包括（边界拼接），滤波器，增强，（放大），灰度图转换，去噪，二值化
：img:待处理图片
"""


def img_transfer(img):
    img = Image.open(img)
    img = img.filter(ImageFilter.MedianFilter(1))  # 滤波器
    img = ImageEnhance.Contrast(img).enhance(1.5)   # 图像增强，enhance参数表示对比度
    img= img.convert('L')   # 灰度图转化
    img= denoisy(img)
    img = binary(img, 200)
    img.show()
    return img

if __name__ == "__main__":
    img = sys.argv[1]
    img_transfer(img)
