# _*_ coding:utf-8_*_
import sys, time
from PIL import Image
from PIL import ImageFilter
from PIL import ImageEnhance


def binary(img, threshold):
    """
    二值化处理
    :param img: 待处理图片
    :param threshold:阈值设定
    :return: 处理后图片
    """
    pixdata = img.load()
    w, h = img.size
    for j in range(h):
        for i in range(w):
            if pixdata[i, j] < threshold:
                pixdata[i, j] = 0
            else:
                pixdata[i, j] = 255
    return img


def denoisy(img):
    """
    图片去噪
        像素值>245的领域像素,判别为背景色
        一个像素上下左右四个像素有超过两个属于背景色，该像素就是目标点，否则就是噪声
    :param img: 待处理图片
    :return: 处理后图片
    """
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


def img_transfer(img):
    """
    图片转化，包括（边界拼接），滤波器，增强，（放大），灰度图转换，去噪，二值化
    :param img:待处理图片
    :return:处理后图片
    """
    # img = Image.open(img)
    # img.show()
    # img = img.rotate(10)
    w, h = img.size
    w *= 1.5
    h *= 1.5
    img = img.resize((int(w), int(h)))

    img = img.filter(ImageFilter.MedianFilter(1))   # 滤波器
    img = ImageEnhance.Contrast(img).enhance(1.5)   # 图像增强，enhance参数表示对比度
    img = ImageEnhance.Sharpness(img).enhance(1.5)  # 图片锐化
    img = img.convert('L')  # 灰度图转化
    img = denoisy(img)
    img = binary(img, 200)

    # img = ImageEnhance.Sharpness(img).enhance(2)
    # print(img.size)
    # img = ImageEnhance.Sharpness(img).enhance(1.5)
    # img = ImageEnhance.Contrast(img).enhance(1.5)   # 图像增强，enhance参数表示对比度
    # img = denoisy(img)
    # img = binary(img, 200)
    # img.thumbnail(size) # 只支持按比例缩小
    img_name = str(time.time()) + ".jpg"
    # img.save(img_name, mimetype='image/jpeg')
    # print(img.size)
    # img.show()
    return img

if __name__ == "__main__":
    img = sys.argv[1]
    img = Image.open(img)
    # img_transfer(img)
