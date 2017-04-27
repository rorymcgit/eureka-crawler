import urllib.request
from bs4 import BeautifulSoup
from crawler.db_translator import Translator
# translator = Translator()

class Crawler():
    def __init__(self, translator = Translator()):
        self.translator = translator
        self.translator.set_environment()

    def crawl(self, url):
        self.url = url
        self.page = urllib.request.urlopen(url).read()
        self.translator.write_url(url)
        #save url at this point to the db

    def return_content(self):
        print(self.page)
        self.soup = BeautifulSoup(self.page, "html.parser")
        self.webpage_title = self.soup.title.string
        self.translator.write_urls_and_titles(self.url, self.webpage_title)
        # save url and self.webpage_title to another database table

# crawler = Crawler()
# crawler.crawl('https://www.webpagetest.org/')
