#!/usr/bin/python3

import os

from PIL import Image
from bs4 import BeautifulSoup

from search.model.javMovie import JavMovie
from search.net.httpUitls import *


class JavTool:
    webRoot = "https://www.cdnbus.in/"

    def __init__(self, root):
        self.webRoot = root

    def getJavInfo(self, code):
        url = self.webRoot + code
        avResponse = getResponse(url)
        print(avResponse.status)
        html = avResponse.read().decode('utf-8')
        soup = BeautifulSoup(html, 'html.parser')

        # imageNode
        a_img_node = soup.find('a', class_='bigImage')
        img_node = a_img_node.find('img')
        # title
        img_title = img_node.get("title")
        # image
        image = a_img_node.get("href")
        # actress
        actresses = []
        actress_divs = soup.find_all('div', class_='star-name')
        for div in actress_divs:
            actress_link = div.find('a')
            actresses.append(actress_link.get_text())
        text_node = soup.find_all('span', class_='header')
        code = text_node[0].find_next('span').get_text()
        pdate_span = text_node[1]
        pdate_p = text_node[1].find_previous('p')
        pdate_span.extract()
        pdate = pdate_p.get_text()
        length_span = text_node[2]
        length_p = text_node[2].find_previous('p')
        length_span.extract()
        length = length_p.get_text()
        director = text_node[3].find_next("a").get_text()
        studio = text_node[4].find_next("a").get_text()
        supplier = text_node[5].find_next("a").get_text()
        series = text_node[6].find_next("a").get_text()
        return JavMovie(code, img_title, image, actresses, director, pdate, series, studio, supplier, length)


def makeAcctress(rootpath, jv):
    os.chdir(rootpath)
    # 创建演员
    if os.path.exists(os.curdir + "\\" + jv.getActress()):
        pass
    else:
        os.mkdir(jv.getActress())
    os.chdir(jv.getActress())
    # 创建发行商
    if os.path.exists(os.curdir + "\\" + jv.supplier):
        pass
    else:
        os.mkdir(jv.supplier)
    os.chdir(jv.supplier)
    # 创建相片
    fileName = "[" + jv.getActress() + "]" + " [" + jv.code + "]" + jv.title
    if os.path.exists(os.curdir + "\\" + fileName):
        pass
    else:
        os.mkdir(fileName)
    os.chdir(fileName)
    # 下载图片
    pic_end = ".jpg"
    filepath = os.curdir + "\\" + fileName + pic_end
    download(jv.image, filepath)
    # 图片切割成 png
    img = Image.open(fileName)
    cropped = img.crop((img.width / 2, 0, img.width, img.height))  # (left, upper, right, lower)
    croppedName = fileName.replace(".jpg", '.png')
    cropped.save(croppedName)


# tool = JavTool("https://www.cdnbus.in/")
# jv = tool.getJavInfo("JUY-951")
# rootpath = "e:\\"
# makeAcctress(rootpath, jv)

filename = "E:\友田真希\Madonna\[友田真希] [JUY-951]僕が隣の痴女奥さんに様々な方法で射精管理され続けた一週間 友田真希\[友田真希] [JUY-951]僕が隣の痴女奥さんに様々な方法で射精管理され続けた一週間 友田真希.jpg"