from bs4 import BeautifulSoup
import requests
import sys
import datetime
import threading


def clear_file(name):
    r = open(name, "w")
    r.write(f"product that is cheaper {sys.argv[1]}" + "\n" + "\n")
    r.close()


t = threading.Thread(target=clear_file, args=("result", ))
t.start()
t.join()


class Paraer:

    def __init__(self, url):
        # "https://rozetka.com.ua/ua/shoes_clothes/c1162030/producer=nike/"
        self.price2 = None
        self.url = requests.get(url).text
        self.soup = BeautifulSoup(self.url, "html.parser")
        self.time_1 = datetime.datetime.now()

    def search(self):
        for value in self.soup.find_all("div", class_="goods-tile__inner"):
            price = value.find("span", class_="goods-tile__price-value").text
            self.price2 = price.replace('\xa0', '')
            if int(self.price2) < int(sys.argv[1]):
                href = value.find("a").get("href")
                req = requests.get(href + "characteristics/").text
                soup2 = BeautifulSoup(req, "html.parser")
                for charact in soup2.find_all("main", class_="product-tabs__content"):
                    print(charact.get_text())
                    end = charact.get_text()
                    with open("result", "a") as f:
                        f.write(end + "\n")
            else:
                print("There are no products matching your request")
                time_2 = datetime.datetime.now()
                time_all = time_2 - self.time_1
                with open("result", "a") as f:
                    f.write(f"time_work: {str(time_all)}" + '\n')
    
    def info(self):
        if int(self.price2) >= int(sys.argv[1]):
            print("There are no products matching your request")


parser = Paraer("https://rozetka.com.ua/ua/shoes_clothes/c1162030/producer=nike/")
parser.search()
parser.info()
