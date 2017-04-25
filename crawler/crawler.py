import requests
from bs4 import BeautifulSoup

class Crawler():
    def crawl(self, url):
        self.response_page = requests.get(url)
        # print(self.page)

    def return_content(self):
        print(type(self.response_page.text))
        # soup = BeautifulSoup(self.response_page.text)
