from lxml import etree

if __name__ == '__main__':
    with open("./test1.html", "r+", encoding="utf-8") as f:
        data = f.read()

    # print(data)
    html = etree.HTML(data)

    # 获取body的所有子节点
    body_children = html.xpath("head")
    print(body_children)

    # 获取body节点
    body = html.xpath("/html/body")[0]
    print(etree.tostring(body, encoding="utf-8").decode("utf-8"))

    # 获取所有的标题
    titles = html.xpath("//div[@class='item']//h3")
    for title in titles:
        print(etree.tostring(title, encoding="utf-8").decode("utf-8"))

    titles_text = html.xpath("//div[@class='item']//h3/text()")
    for title_text in titles_text:
        print(title_text)

    # 获取所有的时间
    times = html.xpath("//div[@class='description']/p[@class='calendar']/em[@class='t']")
    for time in times:
        print(etree.tostring(time, encoding="utf-8").decode("utf-8"))

    times_text = html.xpath("//div[@class='description']/p[@class='calendar']/em[@class='t']/text()")
    for time_text in times_text:
        print(time_text)

    # 获取所有的编号
    views = html.xpath("//div[@class='description']/p[@class='view']/em[@class='t']")
    for view in views:
        print(etree.tostring(view, encoding="utf-8").decode("utf-8"))

    views_text = html.xpath("//div[@class='description']/p[@class='view']/em[@class='t']/text()")
    for view_text in views_text:
        print(view_text)

    data = html.xpath('/html/body/div/div')
