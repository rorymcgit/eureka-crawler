from bs4 import BeautifulSoup

class Parser():
    def create_soup_and_save_content(self, page):
        soup = BeautifulSoup(page, "html.parser", from_encoding="UTF-8")
        return self.parse_webpage_content(soup)

    def parse_webpage_content(self, soup):
        webpage_title = self.find_webpage_title(soup)
        webpage_description = self.find_webpage_metadata(soup, 'description')
        webpage_keywords = self.find_webpage_metadata(soup, 'keywords')
        if self.empty_titles_and_descriptions(webpage_title, webpage_description):
            return {}
        else:
            return {"title": webpage_title, "description": webpage_description, "keywords": webpage_keywords}


    def find_webpage_title(self, soup):
        return soup.title.string if soup.title else ''

    def find_webpage_metadata(self, soup, name):
        try:
            return soup.find("meta", {"name": name})['content']
        except:
            return ''

    def empty_titles_and_descriptions(self, title, description):
        return title == "" and description == ""


# self.parser.create_soup_and_save_content(self.page)
