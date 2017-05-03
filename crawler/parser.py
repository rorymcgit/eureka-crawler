from bs4 import BeautifulSoup

class Parser():
    def soupify_page(self, page):
        return BeautifulSoup(page, "html.parser", from_encoding="UTF-8")

    def create_soup_and_save_content(self, page):
        return self.parse_webpage_content(self.soupify_page(page))

    def create_soup_and_save_weburls(self, page):
        return self.parse_webpages_links(self.soupify_page(page))

    def parse_webpage_content(self, soup):
        webpage_title = self.find_webpage_title(soup)
        # print(webpage_title)
        webpage_description = self.find_webpage_metadata(soup, 'description')
        webpage_keywords = self.find_webpage_metadata(soup, 'keywords')
        if self.check_empty_titles_and_descriptions(webpage_title, webpage_description):
            return {}
        else:
            return {"title": webpage_title,
                    "description": webpage_description,
                    "keywords": webpage_keywords}

    def parse_webpages_links(self, soup):
        webpage_urls = []
        for link in soup.find_all('a', href=True):
            webpage_urls.append(link['href'])
        return webpage_urls

    def find_webpage_title(self, soup):
        return soup.title.string if soup.title else ''

    def find_webpage_metadata(self, soup, name):
        try:
            return soup.find("meta", {"name": name})['content']
        except TypeError:
            return ''

    def check_empty_titles_and_descriptions(self, title, description):
        return title == "" and description == ""
