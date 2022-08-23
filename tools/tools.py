import datetime

# 从列表中获取指定值，默认索引值为0，默认值为空


def getFromList(list, index=0, default=""):
    if not list:
        return default
    else:
        return list[index]


def checkLastNews(newNews, oldNews):
    keys = oldNews.keys()
    if "date" not in keys:
        return newNews["title"][-4:] == oldNews["title"][-4:]
    else:
        return newNews["date"] == oldNews["date"] and newNews["title"][-3:] == oldNews["title"][-3:]


def getYMD():
    today = datetime.datetime.now()
    year = today.year
    month = today.month
    day = today.day
    return year, month, day
