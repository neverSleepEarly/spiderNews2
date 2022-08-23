from request.requestHttp import *
from parse.parseHtml import parseNewsListNY, parseNewsContentNY
from lxml import etree

if __name__ == '__main__':
    WSJURL = "https://cn.wsj.com/{section}/{pageNum}"
    sections = {"国际": "world", "中国": "china/", "商业与经济": "business", "镜头": "",  }
    pageNum = 1
    oldNews = {"title": "中国“锁台”军演适得其反？"}

    # 爬取页数
    pageNum = 1
    maxPage = 50

    # 新闻字典
    newsTotalList = []

    STOP_FLAG = [False]
    while not STOP_FLAG[0]:
        response = getHttpResponse(NYChineseURL.format(section=sections["中国"], pageNum=pageNum))
        # print(type(response))
        html = etree.HTML(response.text)
        # print(type(html))
        newsTotalList.extend(parseNewsListNY(html, oldNews, STOP_FLAG))

        if pageNum == maxPage:
            break
        else:
            # 页码加1
            pageNum += 1

    for newsDict in newsTotalList:
        print(newsDict["title"])
        response = getHttpResponse(newsDict["completeLink"])
        html = etree.HTML(response.text)
        otherInfo = parseNewsContentNY(html)
        newsDict.update(otherInfo)



