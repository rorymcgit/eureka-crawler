import urllib.request
from bs4 import BeautifulSoup
from crawler.db_translator import Translator

class Crawler():
    def __init__(self, translator = Translator()):
        self.translator = translator
        self.translator.set_environment()

    def crawl(self, url):
        self.url = url
        self.page = urllib.request.urlopen(url).read()
        self.translator.write_url(url)

    def return_content(self):
        self.soup = BeautifulSoup(self.page, "html.parser")
        self.webpage_title = self.soup.title.string
        self.save_found_weburls()
        self.translator.write_urls_and_titles(self.url, self.webpage_title)

    def save_found_weburls(self):
        self.webpage_urls = []
        for link in self.soup.find_all('a', href=True):
            self.webpage_urls.append(link['href'])
        self.translator.prepare_urls_for_writing_to_db(self.webpage_urls)




# crawler = Crawler()
# crawler.crawl('https://www.webpagetest.org/')
# crawler.return_content()
