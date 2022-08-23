import requests
from bs4 import BeautifulSoup
from lxml import etree
from parse.parseHtml import *
from request.requestHttp import getHttpResponse

if __name__ == '__main__':
    url = "https://www.zaobao.com.sg/global"

    response = getHttpResponse(url)
    html = etree.HTML(response.text)

    parseIndexZaoBao(html)

    # oldNews = {"title": "习近平李克强致电慰问岸田文雄感染新冠"}
    #
    # formatUrl = "https://www.rfi.fr/cn/档案资料库/{year}/{month}/{day}--"
    #
    # year, month, day = getYMD()
    #
    # count = 0
    # maxDay = 5
    # # 新闻字典
    # newsTotalList = []
    #
    # stopFlag = [False]
    # while (not stopFlag[0]) and count != maxDay:
    #     url = formatUrl.format(year=year, month=month, day=day)
    #     response = getHttpResponse(url)
    #     html = etree.HTML(response.text)
    #
    #     newsTotalList.extend(parseNewsListRFI(html, breakPoint=oldNews, stopFlag=stopFlag))
    #
    #     year, month, day = getYMD(-count)
    #
    #     count += 1
    #
    # for newsDict in newsTotalList:
    #     print(newsDict["title"])
    #     response = getHttpResponse(newsDict["completeLink"])
    #     html = etree.HTML(response.text)
    #     otherInfo = parseNewsContentRFI(html)
    #     newsDict.update(otherInfo)
    #     print(newsDict)
