import urllib.request
from bs4 import BeautifulSoup
from crawler.db_translator import Translator

class Crawler():
    def crawl(self, url):
        self.page = urllib.request.urlopen(url).read()
        #save url at this point to the db


    def return_content(self):
        self.soup = BeautifulSoup(self.page, "html.parser")
        self.webpage_title = self.soup.title.string
        # save url and self.webpage_title to another database table
