import requests


def getHttpResponse(url):
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:88.0) Gecko/20100101 Firefox/88.0',
               "content-type": "application/json; charset=UTF-8",
               "Connection": "keep-alive"
               }

    cookie = {
        "_am_sp_djcsid.e862": "64137bfe-acb4-4182-b0fb-35002342a3ae.1661129338.4.1661175368.1661166400.901d7c2c-71f9-43fb-97f7-c591df596b1c",
        "ntvSession": "{}",
        "ResponsiveConditional_initialBreakpoint": "lg",
        "_am_sp_djcsses.e862": "*",

    }
    try:
        response = requests.get(url, headers=headers, cookies=cookie)
    except Exception as e:
        print(e)
    return response