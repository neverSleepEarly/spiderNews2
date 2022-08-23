from tools.tools import *

# 分析美国之音新闻列表页
def parseNewsListVOA(html, breakPoint):
    baseNewsUrl = "https://www.voachinese.com"

    # 网站时间
    timeOfWeb = html.xpath("//h2[@class='date calendar-component__date']/text()")[0]
    # print(timeOfWeb)

    # 获取 <div class="media-block">，内容包裹节点
    divMediaBlockWrap = \
        html.xpath(
            "//div[@class='col-xs-12 col-md-8 col-lg-8 pull-left content-offset']//div[@class='media-block-wrap']")[
            0]
    divMediaBlocks = divMediaBlockWrap.xpath(".//div[@class='media-block ']")

    newsList = []

    for divMediaBlock in divMediaBlocks:
        newsDict = {}

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

            # 获取视频标志节点：<span class="ico ico-video ico--media-type">

            if len(divMediaBlock.xpath("./a/span")) > 0:
                newsType = "video"
            else:
                newsType = "article"

        except Exception as e:
            print(e)

        newsDict["date"] = newsDate
        newsDict["partLink"] = newsPartLink
        newsDict["completeLink"] = newsCompleteLink
        newsDict["title"] = newsTitle
        newsDict["desc"] = newsDesc
        newsDict["type"] = newsType

        if checkLastNews(newsDict, breakPoint):
            global STOP_FLAG
            STOP_FLAG = True
            print(STOP_FLAG)
            break

        newsList.append(newsDict)
    return newsList


# 分析纽约时报新闻列表页
def parseNewsListNY(html, breakPoint, stopFlag):
    baseNewsUrl = "https://cn.nytimes.com/"

    # 网站时间
    # timeOfWeb =
    # print(timeOfWeb)

    newsList = []

    # 获取头条新闻

    # 获取其他新闻包裹节点，<div class="sectionAutoList columnAplusB ">
    divBasicList = getFromList(html.xpath("//div[@class='sectionAutoList columnAplusB ']/div[@class='basic-list']"))

    # 获取所有新闻项，<li class="autoListStory first">
    liAutoListStoryList = divBasicList.xpath(".//li")

    newsList = []
    for li in liAutoListStoryList:
        newsDict = {}

        try:
            # 获取标题节点，<h3 class="regularSummaryHeadline">
            aTitle = getFromList(li.xpath("./h3[@class='regularSummaryHeadline']/a"))
            newsTitle = getFromList(aTitle.xpath("@title"))

            # 获取链接
            newsPartLink = getFromList(aTitle.xpath("@href"))
            newsCompleteLink = baseNewsUrl + newsPartLink

            # 获取作者节点，<span class="en_byline">ANDREW E. KRAMER</span>
            newsAuthor = getFromList(li.xpath("./h6[@class='byline;']/span/text()"))

            # 获取简介
            newsDesc = getFromList(li.xpath("./p[@class='summary']/text()"))
        except Exception as e:
            print(e)

        newsDict["partLink"] = newsPartLink
        newsDict["completeLink"] = newsCompleteLink
        newsDict["title"] = newsTitle
        newsDict["desc"] = newsDesc
        newsDict["author"] = newsAuthor

        if checkLastNews(newsDict, breakPoint):
            stopFlag[0] = True
            print(stopFlag)
            break
        print(newsDict)
        newsList.append(newsDict)
    print(newsList)
    return newsList


# 分析美国之音新闻详情页
def parseNewsContentVOA(html, newsDict):
    newsDict = {}
    try:
        print(newsDict["type"])
        if newsDict["type"] == "article":
            # 获取新闻发表时间节点，<span class="date-time">
            spanTime = getFromList(html.xpath("//span[@class='date' and @title='中国时间']"))
            newsTimeString = getFromList(spanTime.xpath("./time/text()")).replace("\n", "")
            newsTimeDateFormat = getFromList(spanTime.xpath("./time/@datetime"))

            # 获取新闻图片url
            divCoverMedia = getFromList(html.xpath("//div[@class='cover-media']"))
            newsPicUrl = getFromList(divCoverMedia.xpath(".//img//@src"))
            newsPicTitle = getFromList(divCoverMedia.xpath(".//img/@alt"))

            # 获取新闻内容包裹节点，<div class="wsw">
            newsContentContainer = getFromList(html.xpath("//div[@class='wsw']"))
            # 获取新闻内容
            newContent = "\n".join(newsContentContainer.xpath(".//p/text()")).replace("\n", "", 1)

            newsDict["time"] = newsTimeString
            newsDict["timeFormat"] = newsTimeDateFormat
            newsDict["picUrl"] = newsPicUrl
            newsDict["picTitle"] = newsPicTitle
            newsDict["content"] = newContent
        else:
            # 获取视频url节点，<video ...>
            newsVideoUrl = getFromList(html.xpath("//a[@class='c-mmp__fallback-link']/@href"))
            newsDict["videoUrl"] = newsVideoUrl
        # 评论区（略）
    except Exception as e:
        print(e)


# 爬取纽约时报新闻详情页
def parseNewsContentNY(html):
    newsDict = {}
    try:
        # 获取新闻内容的包裹节点，<article class="article-content font-normal">
        articleContent = getFromList(html.xpath("//article[@class='article-content font-normal']"))


        # 获取新闻发表时间节点，<span class="date-time">
        time = getFromList(articleContent.xpath("./div[@class='article-header']/div[@class='byline-row']//time"))
        newsTime = getFromList(time.xpath("./@pudate"))
        # time.xpath("./@datetime")

        # 获取新闻图片url
        figure = getFromList(html.xpath("//figure[@class='article-span-photo']"))
        newsPicUrl = getFromList(figure.xpath("./img/@src"))
        newsPicTitle = getFromList(figure.xpath("./img/@alt"))

        # 获取新闻内容包裹节点，<div class="wsw">
        divArticlePartialList = html.xpath("//section[@class='article-body']//div[@class='article-partial']")

        newContent = ""
        for divArticlePartial in divArticlePartialList:
            # 获取新闻内容
            paragraph = "".join(divArticlePartial.xpath("./div[@class='article-body-item col-lg-5']//div[@class='article-paragraph']//text()"))
            paragraph += "\n"
            newContent += paragraph

        newsDict["time"] = newsTime
        newsDict["timeFormat"] = newsTime
        newsDict["picUrl"] = newsPicUrl
        newsDict["picTitle"] = newsPicTitle
        newsDict["content"] = newContent

        # 获取视频url节点，<video ...>
        newsVideoUrl = getFromList(html.xpath("//a[@class='c-mmp__fallback-link']/@href"))
        newsDict["videoUrl"] = newsVideoUrl
    # 评论区（略）
    except Exception as e:
        print(e)
    return newsDict


# 分析华盛顿时报首页，获取各板块链接
def parseIndexWSJ(html):
    baseUrl = "https://cn.wsj.com"
    sections = []
    try:
        # 获取导航栏节点
        navContainer = getFromList(html.xpath("//header[@role='banner']/nav"))
        liList = navContainer.xpath(".//li")

        for li in liList:
            section = {}
            # 获取各板块的链接
            sectionLink = getFromList(li.xpath("./a/@href"))
            if not sectionLink.startswith("https://"):
                sectionLink = baseUrl + sectionLink
            # 获取各版块名称
            sectionName = getFromList(li.xpath("./a/text()"))
            section[sectionName] = sectionLink
            sections.append(section)
    except Exception as e:
        print(e)

    return sections


# 分析华盛顿日报新闻列表页
def parseNewsListWSJ(html, breakPoint, stopFlag):
    baseNewsUrl = "https://cn.nytimes.com/"



    ol = html.xpath("//ol")

    print(ol)
    # newsList = []
    # for article in ol:
    #     newsDict = {}
    #     try:
    #         # 获取标题节点，<h3 class="regularSummaryHeadline">
    #         newsTitle = getFromList(article.xpath(".//h3//span//text()"))
    #         # 获取链接
    #         newsCompleteLink = getFromList(article.xpath(".//h3/a/@href"))
    #         # 获取时间
    #         newsTime = getFromList(article.xpath(".//div[2]/p/text()"))
    #         # 获取简介
    #         newsDesc = getFromList(article.xpath("./p/span/text()"))
    #     except Exception as e:
    #         print(e)
    #
    #     newsDict["completeLink"] = newsCompleteLink
    #     newsDict["title"] = newsTitle
    #     newsDict["desc"] = newsDesc
    #     newsDict["time"] = newsTime
    #
    #     if checkLastNews(newsDict, breakPoint):
    #         stopFlag[0] = True
    #         print(stopFlag)
    #         break
    #     print(newsDict)
    #     newsList.append(newsDict)
    # print(newsList)
    # return newsList


# 分析法广中文网新闻列表页
def parseNewsListRFI(html, breakPoint, stopFlag):
    baseNewsUrl = "https://www.rfi.fr/"

    newsList = []

    # 获取新闻包裹节点，<div class="sectionAutoList columnAplusB ">
    ulArchive = getFromList(html.xpath("//div[@class='o-archive-day']//ul[@class='o-archive-day__list']"))

    # 获取所有新闻项，<li class="autoListStory first">
    aArchieve = ulArchive.xpath("./li/a")

    newsList = []
    for a in aArchieve:
        newsDict = {}

        try:
            # 获取标题节点，<h3 class="regularSummaryHeadline">
            newsTitle = getFromList(a.xpath("./text()"))

            # 获取链接
            newsPartLink = getFromList(a.xpath("./@href"))
            newsCompleteLink = baseNewsUrl + newsPartLink

        except Exception as e:
            print(e)

        newsDict["partLink"] = newsPartLink
        newsDict["completeLink"] = newsCompleteLink
        newsDict["title"] = newsTitle

        if checkLastNews(newsDict, breakPoint):
            stopFlag[0] = True
            print(stopFlag)
            break
        print(newsDict["title"])
        newsList.append(newsDict)
    return newsList


# 爬取法广中文网新闻详情页
def parseNewsContentRFI(html):
    newsDict = {}
    try:
        # 获取新闻内容的包裹节点，<article class="article-content font-normal">
        articleContent = getFromList(html.xpath("//div[@class='t-content t-content--article']/article"))

        # 获取新闻发表时间节点
        time = getFromList(articleContent.xpath("./div[@class='t-content__dates']/p[@class='m-pub-dates']/span/time"))
        newsFormatTime = getFromList(time.xpath("./@datetime"))
        newsTime = timeFormat2Time(newsFormatTime)

        # 获取新闻图片url
        figure = getFromList(articleContent.xpath("./div[@class='t-content__main-media']/figure"))
        newsMediaType = getFromList(figure.xpath("./picture/source/@type"))
        srcset = getFromList(figure.xpath("./picture/img/@srcset"))
        newsPicUrl = srcset.split(",")[-1].split(" ")[0]
        newsPicTitle = getFromList(figure.xpath("./picture/img/@alt"))

        # 获取作者
        # newsAuthor = getFromList(articleContent.xpath(".//div[@class='t-content__authors-tts']//a[@class='m-from-author__name']/text()]"))

        # 获取简介
        newsDesc = getFromList(articleContent.xpath("./p[@class='t-content__chapo']/text()"))

        # 获取新闻内容包裹节点，<div class="wsw">
        pList = articleContent.xpath("./div[@class='t-content__body u-clearfix']/p")

        newContent = ""
        for p in pList:
            # 获取新闻内容
            paragraph = "".join(p.xpath("./text()"))
            paragraph += "\n"
            newContent += paragraph

        newsDict["time"] = newsTime
        newsDict["timeFormat"] = newsTime
        newsDict["MediaType"] = newsMediaType
        # newsDict["author"] = newsAuthor
        newsDict["desc"] = newsDesc
        newsDict["picUrl"] = newsPicUrl
        newsDict["picTitle"] = newsPicTitle
        newsDict["content"] = newContent

    # 评论区（略）
    except Exception as e:
        print(e)
    return newsDict


# 分析联合早报首页，获取各板块链接
def parseIndexZaoBao(html):
    baseUrl = "https://www.zaobao.com.sg"
    sections = []
    try:
        # 获取导航栏节点
        divNav = getFromList(html.xpath("//div[@class='row align-items-center row no-gutters']"))
        divDropdowList = divNav.xpath("./div")

        sections = []
        for div in divDropdowList:
            # 获取一级栏目节点
            firstSectionLink = getFromList(div.xpath("./a/@href"))
            firstSectionName = getFromList(div.xpath("./a/span/text()"))

            # 获取二级栏目节点
            div = div.xpath("./div[@class='dropdown-menu']")
            if len(div) == 0:
                print("no second section")
            else:
                aDropDownItemList = div[0].xpath(".//a[@class='topnav-link dropdown-item']")

                for aDropDownItem in aDropDownItemList:
                    section = {}
                    secondSectionLink = getFromList(aDropDownItem.xpath("./@href"))
                    secondSectionName = getFromList(aDropDownItem.xpath("./text()"))
                    section[firstSectionName + "/" + secondSectionName] = baseUrl + firstSectionLink + secondSectionLink
                    sections.append(section)
                    print(section)
    except Exception as e:
        print(e)

    return sections