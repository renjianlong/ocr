# _*_ coding:utf-8_*_

import sys, time, requests
import pytesseract
import langid
import io
import re
import imgprocess
from PIL import Image


def getIMGText(url, language):
    """
    带语种参数的识别
    :param url: 图片链接
    :param language: 语种
    :return: 识别结果
    """
    img = Image.open(io.BytesIO(requests.get(url).content)).convert('RGB')
    # img.show
    img = imgprocess.img_transfer(img)
    imgname = str(time.time()) + ".jpg"
    # img.save(imgname, mimetype='image/jpeg')
    # img.show()
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
    # img.save(img_name, mimetype='image/jpeg')
    img_text = pytesseract.image_to_string(img)

    lang = langid.classify(img_text)
    return img_text, lang


def getLangCount(c):
    """
    对单个字符计数
    :param c:字符
    :return:list返回计数结果
    """

    i = int(str(c), 16)  # 转换为16进制
    lang_count = [0, 0, 0]

    # 中文字符计数
    if ((int("4E00", 16) <= i <= int("9FFF", 16)) or
            (int("3400", 16) <= i <= int("4DBF", 16)) or

            (int("20000", 16) <= i <= int("2A6DF", 16)) or
            (int("2A700", 16) <= i <= int("2B73F", 16)) or
            (int("2B740", 16) <= i <= int("2B81F", 16)) or
            (int("2B820", 16) <= i <= int("2CEAF", 16)) or
            (int("F900", 16) <= i <= int("FAFF", 16)) or
            (int("2F800", 16) <= i <= int("2FA1F", 16))):
        lang_count[0] += 1

    # 维文字符计数
    if ((int("0600", 16) <= i <= int("06FF", 16)) or
            (int("0750", 16) <= i <= int("077F", 16)) or
            (int("FB50", 16) <= i <= int("FDFF", 16)) or
            (int("FE70", 16) <= i <= int("FEFF", 16))):
        lang_count[1] += 1

    # 英文字符计数
    if ((int("0041", 16) <= i <= int("005A", 16)) or
            (int("0061", 16) <= i <= int("007A", 16))):
        lang_count[2] += 1

    return lang_count


def getcount(text):
    """
    统计文本的语种字符计数
    :param text: 文本
    :return: 英、中、维计数结果
    """
    count = [0, 0, 0]
    text = text.replace("\r", "").replace("\n", "").replace(" ", "")
    for t in text:
        # print(t)
        if type(t) == 'int':
            continue
        c = '%04x' % ord(t)
        tempcount = getLangCount(c)
        count[0] += tempcount[0]
        count[1] += tempcount[1]
        count[2] += tempcount[2]
    return count


def gettextLang(url):
    """
    识别语种情况
    :param url:图片链接
    :return:文本及语种识别情况
    """
    chi_text = ""
    eng_text = ""
    uig_text = ""
    img = Image.open(io.BytesIO(requests.get(url).content)).convert('RGB')
    img_name = str(time.time()) + ".jpg"
    # img.save(img_name, mimetype='image/jpeg')
    img = imgprocess.img_transfer(img)
    # 对于图片进行三次识别,依次为中文，英文，维文
    score = []
    # 中文识别得分
    chi_text = pytesseract.image_to_string(img, lang='chi_sim')
    # chi_text = chi_text.replace("\r", "").replace("\n", "").replace(" ", "")
    chi_count = getcount(chi_text)
    # print(chi_count)
    chi_score = float(chi_count[0]/(sum(chi_count, 0) + 1))
    # print(chi_score)
    score.append(chi_score)

    # 英文识别得分
    eng_text = pytesseract.image_to_string(img, lang='eng')
    eng_count = getcount(eng_text)
    eng_score = float(eng_count[2]/(sum(eng_count, 0) + 1))
    # print(eng_count)
    # print(eng_score)
    score.append(eng_score)

    # 维文识别得分
    uig_text = pytesseract.image_to_string(img, lang='uig')
    uig_count = getcount(uig_text)
    uig_score = float(uig_count[1]/(sum(uig_count, 0) + 1))
    # print(uig_count)
    # print(uig_score)
    score.append(uig_score)

    # print(score)
    if max(score) == score[0]:
        return chi_text, "chi_sim"
    elif max(score) == score[1]:
        return eng_text, "eng"
    else:
        return uig_text, "uig"



def main():
    """
    主函数
    :return:识别出的文本（或带语种）
    """
    if len(sys.argv) == 2:
        url = str(sys.argv[1])
        text, lang = gettextLang(url)
        # text = re.sub("[\s+\.\!\/_,$%^*(+\"\']+|[+——！，。？、~@#￥%……&*（）]", str(text))
        # text = text.replace("\r", "").replace("\n", "").replace(" ", "")
        print(text)
        # print(text.encode('utf-8', 'ignore').decode('gbk', 'ignore'))

        # print(type(text))
        print("语种：", lang)
    elif len(sys.argv) == 3:
        url = str(sys.argv[1])
        lang = sys.argv[2]
        text = getIMGText(url, lang)
        # print(text.encode('utf-8', 'ignore').decode('gbk', 'ignore'))
        print(text)
    else:
        print('paraments error!')
        sys.exit(1)


if __name__ == "__main__":
    main()
