import urllib.request
from bs4 import BeautifulSoup
from crawler.db_translator import Translator

class Crawler():
    def __init__(self, translator = Translator()):
        self.translator = translator

    def crawl(self, url):
        self.url = url
        self.page = urllib.request.urlopen(url).read()
        self.translator.write_url(url)

    def return_all_content(self):
        soup = BeautifulSoup(self.page, "html.parser")
        self.save_found_weburls(soup)
        self.webpage_title = self.find_webpage_title(soup)
        self.webpage_description = self.find_webpage_description(soup)
        self.webpage_keywords = soup.find("meta", {"name":"keywords"})['content']
        self.translator.write_urls_and_content(self.url, self.webpage_title, self.webpage_description, self.webpage_keywords)

    def save_found_weburls(self, soup):
        self.webpage_urls = []
        for link in soup.find_all('a', href=True):
            self.webpage_urls.append(link['href'])
        self.translator.prepare_urls_for_writing_to_db(self.webpage_urls)

    def find_webpage_title(self, soup):
        if soup.title == None:
            return ''
        else:
            return soup.title.string

    def find_webpage_description(self, soup):
        try:
            return soup.find("meta", {"name":"description"})['content']
        except:
            return ''

# crawler = Crawler()
# crawler.crawl("file:///Users/vicky/Programmes/beetlecrawler/spec/website/test.html")
# crawler.return_all_content()
