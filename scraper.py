import requests
from bs4 import BeautifulSoup
import re
import json
import sys
# import paho.mqtt.client as mqtt


# MQTT broker add
# broker_address="ha1.home"
# client=mqtt.Client("scraperpy")
#
# client.connect(broker_address)





def extract_url(url):

    if url.find("www.amazon.in") != -1:
        index = url.find("/dp/")
        if index != -1:
            index2 = index + 14
            url = "https://www.amazon.in" + url[index:index2]
        else:
            index = url.find("/gp/")
            if index != -1:
                index2 = index + 22
                url = "https://www.amazon.in" + url[index:index2]
            else:
                index = url.find("/gp/product/")
                if index != -1:
                    index2 = index + 22
                    url = "https://www.amazon.in" + url[index:index2]
                else:
                    url = None
    else:
        url = None
    return url



def get_converted_price(price):
    # stripped_price = price.strip("₹ ,")
    # replaced_price = stripped_price.replace(",", "")
    # find_dot = replaced_price.find(".")
    # to_convert_price = replaced_price[0:find_dot]
    # converted_price = int(to_convert_price)
    converted_price = float(re.sub(r"[^\d.]", "", price)) # Thanks to https://medium.com/@oorjahalt
    return converted_price



def get_product_details(url):
    headers = {
'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36',
'Accept' : 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
'Accept-Language' : 'en-US,en;q=0.5',
'Accept-Encoding' : 'gzip',
'DNT' : '1', # Do Not Track Request Header
'Connection' : 'close'
}
    details = {"name": "", "price": 0, "deal": True, "url": ""}
    _url = extract_url(url)
    if _url == "":
        details = None
    else:
        page = requests.get(url, headers=headers)
        soup = BeautifulSoup(page.content, 'html.parser')  # changed
        title = soup.find("span", id="productTitle")
        price = soup.find("span", class_="a-offscreen")
        # price = soup.find(id="priceblock_ourprice").get_text()
        # print(title)
        # print(price)
        if price is None:
            # price = soup.find("span", class_="a-offscreen").text
            details["deal"] = False
        if title is not None and price is not None:
            details["name"] = title.get_text().strip()
            # details["name"] = title.strip()
            details["price"] = get_converted_price(price.get_text())
            details["url"] = url
        else:
            return None

    json1 = json.dumps(details, indent = 5)
    return json1

# def get_data():
#     f=open("data.txt","r")
#     f1=f.readlines()
#     print(f1)
# #     print("zzz")
#     for x in f1:
#         print(x)
#         print(get_product_details(x))

# print(get_product_details("https://www.amazon.in/dp/B08FB2LNSZ"))

#Running script via pythonshell node on Node-red
print(get_product_details(sys.argv[1]))




# get_data()
#print(get_product_details("https://www.amazon.in/Harpic-Original-Powerplus-Pack/dp/xxxxxxxxx"))
#   productTitle
# priceblock_ourprice
# id=“priceblock_dealprice”
