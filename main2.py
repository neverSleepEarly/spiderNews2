import os

import requests
from bs4 import BeautifulSoup


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
    url = 'http://www.seaforces.org/usnships/cg/CG-71-USS-Cape-St-George.htm'

    save_bath_path = 'C:\\Users\\admin\Desktop' #船只种类的上级目录
    category = "\\Guided Missile Cruisers (CG, CGN)\\Ticonderoga class CG" #船只种类，单独作为一个目录
    ship_name = "\\CG 71 USS Cape St. George" #船只名称，单独作为一个目录

    save_path = save_bath_path + category + ship_name
    pic_urls = crawlPicUrl(url)

    count = 0
    for pic_url in pic_urls:
        file_name = pic_url.split("/")[-1]
        downloadPic(pic_url, save_path, file_name)
        count += 1
