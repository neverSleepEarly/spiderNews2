import requests
from bs4 import BeautifulSoup
from urllib.request import urlretrieve
import os, stat
import urllib.request


def getShipCategoryUrls(url):
    wb_data = requests.get(url)
    soup = BeautifulSoup(wb_data.text, "lxml")
    span_list = soup.find_all('span', class_="auto-style13")

    ship_categories = []
    for span in span_list:
        ship_category = {}
        if span.a != None and span.a.strong != None:
            ship_category["category"] = span.a.strong.text
            ship_category["link"] = span.a.get("href")
            ship_categories.append(ship_category)
            print(ship_category)

    return ship_categories


def getShipUrls(url):
    wb_data = requests.get(url)
    print(wb_data)
    soup = BeautifulSoup(wb_data.text, "lxml")
    span_list = soup.find_all('span', class_="auto-style35")

    ships = []
    for span in span_list:
        ship = {}
        if span.strong != None:
            ship["Port Number"] = span.strong.text.replace("\n", "").replace("\t", "").strip()
        if span.a != None:
            ship["name"] = span.a.strong.text
            ship["link"] = span.a.get("href")
        else:
            ship["name"] = ""
            ship["link"] = ""
        print(ship)
        ships.append(ship)

    return ships


def crawlPicUrl(base_url):
    wb_data = requests.get(base_url)
    soup = BeautifulSoup(wb_data.text, "lxml")
    p_list = soup.find_all('img')
    pic_url_list = []
    for p in p_list:
        pic_url = p.get('src')
        pic_url_list.append(combineUrl(base_url, pic_url))
        print(combineUrl(base_url, pic_url))
    return pic_url_list


def combineUrl(base_url, pic_url):
    return "/".join(base_url.split("/")[:-1]) + "/" + pic_url


def downloadPic(img_url, file_directory, file_name):
    # 请求头
    headers = {
        # 用户代理
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36'
    }

    try:
        # 是否有这个路径
        if not os.path.exists(file_directory):
            # 创建路径
            os.makedirs(file_directory)
            # 获得图片后缀
        file_suffix = os.path.splitext(img_url)[1]

        file_path = file_directory + "\\" + file_name
        tem = requests.get(img_url, headers=headers, timeout=2)
        with open(file_path, "wb") as f:
            f.write(tem.content)
        print(file_path)
    except Exception as e:
        print(e)



if __name__ == '__main__':
    start_ulr = 'https://www.seaforces.org/usnships/first.htm'
    save_base_path = r'C:\Users\admin\Desktop\ship'

    ship_category_urls = getShipCategoryUrls(start_ulr)

    for ship_category_url in ship_category_urls:
        save_base_path2 = save_base_path + "\\" + ship_category_url["category"]

        ship_urls = {}
        ship_urls = getShipUrls(ship_category_url["link"])

        for ship in ship_urls:
            name = ship["name"]
            port_number = ship["Port Number"]
            link = ship["link"]

            count = 0
            save_base_path3 = save_base_path2 + "\\" + name + " " + port_number

            if link != "":
                pic_urls = crawlPicUrl(link)

                for pic_url in pic_urls:
                    file_name = pic_url.split("/")[-1]
                    downloadPic(pic_url, save_base_path3, file_name)
                    count += 1
