import requests
from bs4 import BeautifulSoup
from lxml import etree


def getHttpResponse(url):
    try:
        response = requests.get(url)
    except Exception as e:
        print(e)
    return response


def checkLastNews(newNews, oldNews):
    return newNews["date"] == oldNews["date"] and newNews["title"][-3:] == oldNews["title"][-3:]


# 从列表中获取指定值，默认索引值为0，默认值为空
def getFromList(list, index=0, default=""):
    if not list:
        return default
    else:
        return list[index]


def parseNewsList(html, breakPoint):

    baseNewsUrl = "https://www.voachinese.com"

    # 网站时间
    timeOfWeb = html.xpath("//h2[@class='date calendar-component__date']/text()")[0]
    # print(timeOfWeb)

    # 获取 <div class="media-block">，内容包裹节点
    divMediaBlockWrap = \
    html.xpath("//div[@class='col-xs-12 col-md-8 col-lg-8 pull-left content-offset']//div[@class='media-block-wrap']")[
        0]
    divMediaBlocks = divMediaBlockWrap.xpath(".//div[@class='media-block ']")

    newsList = []
    newsDict = {}
    for divMediaBlock in divMediaBlocks:
        # 获取 <div class="media-block__content media-block__content--h">，不包含图片的内容包裹，
        # media-block__content media-block__content--h media-block__content--h-xs是非顶部class值
        divContentBlock = divMediaBlock.xpath("./div")[0]

        # 获取新闻信息
        try:
            # 获取 <span class="date date--mb date--size-2/3" title="中国时间">，时间节点，顶部的为date--size-2
            newsDate = getFromList(divContentBlock.xpath("./span/text()")).strip()

            # 获取链接节点：<a ...>
            newsPartLink = getFromList(divContentBlock.xpath("./a/@href")).strip()
            # 拼接完整链接
            newsCompleteLink = baseNewsUrl + newsPartLink

            # 获取标题节点：<h4 class=...>
            newsTitle = getFromList(divContentBlock.xpath("./a//h4/text()")).replace("\n", "").strip()

            # 获取简介节点：<p ...>
            newsDesc = getFromList(divContentBlock.xpath("./a//p/text()")).strip()
        except Exception as e:
            print(e)

        newsDict["date"] = newsDate
        newsDict["partLink"] = newsPartLink
        newsDict["completeLink"] = newsCompleteLink
        newsDict["title"] = newsTitle
        newsDict["desc"] = newsDesc

        if checkLastNews(newsDict, breakPoint):
            global STOP_FLAG
            STOP_FLAG = True
            print(STOP_FLAG)
            break

        print(newsDict)
        newsList.append(newsDict)
    return newsList


def parseNewsContent(html, newsDict):
    # 获取新闻发表时间节点，<span class="date-time">
    spanTime = getFromList(html.xpath("//span[@class='date' and @title='中国时间']"))
    newsTimeString = getFromList(spanTime.xpath("./time/text()")).replace("\n", "")
    newsTimeDateFormat = getFromList(spanTime.xpath("./time/@datetime"))

    # 获取新闻内容包裹节点，<div class="wsw">
    newsContentContainer = getFromList(html.xpath("//div[@class='wsw']"))
    #获取新闻图片url
    divCoverMedia = getFromList(html.xpath("//div[@class='cover-media']"))
    newsPicUrl = getFromList(divCoverMedia.xpath(".//img//@src"))
    newsPicTitle = getFromList(divCoverMedia.xpath(".//img/@alt"))

    # 获取新闻内容
    newContent = "\n".join(newsContentContainer.xpath(".//p/text()")).replace("\n", "", 1)

    # 评论区（略）

    newsDict["time"] = newsTimeString
    newsDict["timeFormat"] = newsTimeDateFormat
    newsDict["picUrl"] = newsPicUrl
    newsDict["picTitle"] = newsPicTitle
    newsDict["content"] = newContent


if __name__ == '__main__':

    VOAChineseURL = "https://www.voachinese.com/z/1739/?p={pageNum}"  # 美国之音中文网新闻要览的url

    oldNews = {"date": "2022年8月21日", "title": "土耳其连续发生交通事故，至少32人死亡"}
    # 爬取页数
    pageNum = 0
    maxPage = 100

    # 新闻字典
    newsList = []

    STOP_FLAG = False
    while not STOP_FLAG:

        response = getHttpResponse(VOAChineseURL.format(pageNum=str(pageNum)))
        # print(type(response))
        html = etree.HTML(response.text)
        # print(type(html))
        print(parseNewsList(html, oldNews))
        newsList.extend(parseNewsList(html, oldNews))

        if pageNum == maxPage:
            break
        else:
            # 页码加1
            pageNum += 1
    print(newsList)

    for newsDict in newsList:
        response = getHttpResponse(newsDict["completeLink"])
        html = etree.HTML(response.text)
        parseNewsContent(html, newsDict)



        # # 网站时间
        # timeOfWeb = html.xpath("//h2[@class='date calendar-component__date']/text()")[0]
        # # print(timeOfWeb)
        #
        # # 获取 <div class="media-block">，内容包裹节点
        # divMediaBlockWrap = html.xpath("//div[@class='col-xs-12 col-md-8 col-lg-8 pull-left content-offset']//div[@class='media-block-wrap']")[0]
        # divMediaBlocks = divMediaBlockWrap.xpath(".//div[@class='media-block ']")
        #
        # for divMediaBlock in divMediaBlocks:
        #     # 获取 <div class="media-block__content media-block__content--h">，不包含图片的内容包裹，
        #     # media-block__content media-block__content--h media-block__content--h-xs是非顶部class值
        #     divContentBlock = divMediaBlock.xpath("./div")[0]
        #
        #     # 获取新闻信息
        #     try:
        #         # 获取 <span class="date date--mb date--size-2/3" title="中国时间">，时间节点，顶部的为date--size-2
        #         newsDate = getFromList(divContentBlock.xpath("./span/text()")).strip()
        #
        #         # 获取链接节点：<a ...>
        #         newsPartLink = getFromList(divContentBlock.xpath("./a/@href")).strip()
        #
        #         # 获取标题节点：<h4 class=...>
        #         newsTitle = getFromList(divContentBlock.xpath("./a//h4/text()")).replace("\n", "").strip()
        #
        #         # 获取简介节点：<p ...>
        #         newsDesc = getFromList(divContentBlock.xpath("./a//p/text()")).strip()
        #     except Exception as e:
        #         print(e)
        #
        #     newsDict["date"] = newsDate
        #     newsDict["partLink"] = newsPartLink
        #     newsDict["title"] = newsTitle
        #     newsDict["desc"] = newsDesc
        #
        #     # 断点检测
        #     if checkLastNews(newsDict, oldNews) or pageNum == maxPage:
        #         STOP_FLAG = True
        #         break
        #
        #     newsList.append(newsDict)
        #     print(newsDict)

