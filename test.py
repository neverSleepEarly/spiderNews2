import requests
from bs4 import BeautifulSoup
from lxml import etree
from parse.parseHtml import *
from request.requestHttp import getHttpResponse

if __name__ == '__main__':
    oldNews = {"title": "杜金之女暴死与俄乌间的“超限战"}

    formatUrl = "https://www.rfi.fr/cn/档案资料库/{year}/{month}/{day}--"

    year, month, day = getYMD()
    url = formatUrl.format(year=year, month=(month - 2), day=day)

    response = getHttpResponse(url)
    html = etree.HTML(response.text)

    stopFlag = [False]
    parseNewsListRFI(html, breakPoint=oldNews, stopFlag=stopFlag)

