# _*_ coding:utf-8_*_

import sys,time, requests
import pytesseract
import langid
import io
from PIL import Image


def getIMGText(url, language):
    """
    带语种参数的识别
    :param url: 图片链接
    :param language: 语种
    :return: 识别结果
    """
    img = Image.open(io.BytesIO(requests.get(url).content)).convert('RGB')
    imgname = str(time.time()) + ".jpg"
    img.save(imgname, mimetype='image/jpeg')
    imgtext = pytesseract.image_to_string(img, lang=language)
    return imgtext


def get_text_lang(url):
    """
    不带语种的识别，仅用来测试
    :param url: 图片链接
    :return: 识别出的文本，语种
    """
    img = Image.open(io.BytesIO(requests.get(url).content)).convert('RGB')
    img_name = str(time.time()) + ".jpg"
    img.save(img_name, mimetype='image/jpeg')
    img_text = pytesseract.image_to_string(img)
    lang = langid.classify(img_text)
    return img_text, lang


# """
# getLangCount():得到各语种的字符计数
# ：c:字符的unicode编码
# """
#
#
# def getLangCount(c):
#     i = int(str(c), 16) #转换为16进制
#     langcount = [0, 0, 0]
#
#     # 中文字符计数
#     if ((int("4E00", 16) <= i <= int("9FFF", 16)) or
#             (int("3400", 16) <= i <= int("4DBF", 16)) or
#             (int("20000", 16) <= i <= int("2A6DF", 16)) or
#             (int("2A700", 16) <= i <= int("2B73F", 16)) or
#             (int("2B740", 16) <= i <= int("2B81F", 16)) or
#             (int("2B820", 16) <= i <= int("2CEAF", 16)) or
#             (int("F900", 16) <= i <= int("FAFF", 16)) or
#             (int("2F800", 16) <= i <= int("2FA1F", 16))):
#         langcount[0] += 1
#
#     # 英文字符计数
#     if ((int("0600", 16) <= i <= int("06FF", 16)) or
#             (int("0750", 16) <= i <= int("077F", 16)) or
#             (int("FB50", 16) <= i <= int("FDFF", 16)) or
#             (int("FE70", 16) <= i <= int("FEFF", 16))):
#         langcount[1] += 1
#
#     # 维文字符计数
#     if ((int("0041", 16) <= i <= int("005A", 16)) or
#             (int("0061", 16) <= i <= int("007A", 16))):
#         langcount[2] += 1
#
#     return langcount
#
#
# """
# gettextLang():语种识别
# :url:图片链接
# """
#
#
# def gettextLang(url):
#     text = []
#     img = Image.open(StringIO(requests.get(url).content)).convert('RGB')
#     imgname = str(time.time()) + ".jpg"
#     img.save(imgname, mimetype='image/jpeg')
#
#     # 对于图片进行三次识别,依次为中文，英文，维文
#     txt = pytesseract.image_to_string(img)
#     chi_text = pytesseract.image_to_string(img, lang='chi_sim')
#     text.append(chi_text)
#
#     eng_text = pytesseract.image_to_string(img,lang='eng')
#     text.append(eng_text)
#
#     uig_text = pytesseract.image_to_string(img, lang='uig')
#     text.append(uig_text)
#
#     # 判断语种
#     chi_count = 0
#     eng_count = 0
#     uig_count = 0
#     for t in text:
#         if type(t) == 'int':
#             continue
#         c = '%04x' % ord(t)
#         count = getLangCount(c)
#         chi_count += count[0]
#         eng_count += count[1]
#         uig_count += count[2]
#     if chi_count == 0 and eng_count == 0 and uig_count != 0:
#         txt = uig_text
#         return txt, "uig"
#     elif chi_count != 0 and eng_count == 0 and uig_count == 0:
#         txt = chi_text
#         return txt, "chi"
#     elif chi_count == 0 and eng_count != 0 and uig_count != 0:
#         txt = eng_text
#         return txt, "eng"
#     else:
#         return txt, "mix"


"""
main():主函数，接受命令行参数，运行程序输出结果

"""


def main():
    if len(sys.argv) == 2:
        url = str(sys.argv[1])
        text, lang = get_text_lang(url)
        print("文本：", text)
        print("语种", lang)
    elif len(sys.argv) == 3:
        url = str(sys.argv[1])
        lang = sys.argv[2]
        text = getIMGText(url, lang)
        print(text)
    else:
        print("paraments error!")
        sys.exit(1)


def run_test():
    """
    测试
    :return:
    """
    url = str(sys.argv[1])
    langclass = langid.classify(url)
    print(langclass)
    return langclass

if __name__ == "__main__":
    main()
