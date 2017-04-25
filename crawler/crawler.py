import requests
from bs4 import BeautifulSoup

class Crawler():
    def crawl(self, url):
        self.response_page = requests.get(url)

    def return_content(self):
        self.soup = BeautifulSoup(self.response_page.text, "html.parser")
        self.webpage_title = self.soup.title.string
