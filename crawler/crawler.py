import urllib.request
from bs4 import BeautifulSoup
from crawler.db_translator import Translator
# translator = Translator()

class Crawler():
    def __init__(self):
        self.translator = Translator()
        self.translator.set_environment()

    def crawl(self, url):
        self.page = urllib.request.urlopen(url).read()
        self.translator.write_url(url)
        #save url at this point to the db

    def return_content(self):
        self.soup = BeautifulSoup(self.page, "html.parser")
        self.webpage_title = self.soup.title.string
        # save url and self.webpage_title to another database table

# crawler = Crawler()
# crawler.crawl('https://www.webpagetest.org/')
