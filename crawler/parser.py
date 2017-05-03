from bs4 import BeautifulSoup

class Parser():
    def __init__(self):
        "hello"

    def parse_webpage_content(self, soup):
        # soup = BeautifulSoup(page, "html.parser", from_encoding="UTF-8")
        self.webpage_title = self.find_webpage_title(soup)
        # self.webpage_description = self.find_webpage_metadata(soup, 'description')
        # self.webpage_keywords = self.find_webpage_metadata(soup, 'keywords')

    def find_webpage_title(self, soup):
        return soup.title.string if soup.title else ''

    # def find_webpage_metadata(self, soup, name):
    #     try:
    #         return soup.find("meta", {"name": name})['content']
    #     except:
    #         return ''
    #
    # def empty_titles_and_descriptions(self, title, description):
    #     return title == "" and description == ""
