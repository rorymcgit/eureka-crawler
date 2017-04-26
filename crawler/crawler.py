import urllib.request
from bs4 import BeautifulSoup

class Crawler():
    def crawl(self, url):
        self.page = urllib.request.urlopen(url).read()

    def return_content(self):
        self.soup = BeautifulSoup(self.page, "html.parser")
        self.webpage_title = self.soup.title.string
