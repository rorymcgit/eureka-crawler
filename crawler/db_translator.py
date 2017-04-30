import sqlalchemy
from sqlalchemy import create_engine, select, insert, MetaData, Table

class Translator():
    def __init__(self, db = 'postgresql://localhost/beetle_crawler_development'):
        self.database_engine = create_engine(db)
        self.connection = self.database_engine.connect()
        metadata = MetaData()
        self.weburls = Table('weburls', metadata, autoload = True, autoload_with = self.database_engine)
        self.weburlsandcontent = Table('weburlsandcontent', metadata, autoload = True, autoload_with = self.database_engine)

    def write_url(self, url):
        if self.url_checker(url):
            url = self.cut_string(url)
            print(url)
            statement = insert(self.weburls).values(weburl = url)
            self.connection.execute(statement)

    def write_urls_and_content(self, url, title, description, keywords):
        statement = insert(self.weburlsandcontent).values(weburl = url, title = title, description = description, keywords = keywords)
        self.connection.execute(statement)

    def prepare_urls_for_writing_to_db(self, weburls):
        for url in weburls:
            if self.get_weburls_table_size() < 1000:
                self.write_url(url)
            else:
                raise Exception

    def get_weburls_table_size(self):
        select_all = select([self.weburls])
        return self.connection.execute(select_all).rowcount

    def url_checker(self, url):
        return self.check_url_beginning(url) and self.check_url_domain(url)

    def check_url_beginning(self, url):
        return url.startswith( 'http' )

    def check_url_domain(self, url):
        return '.co.uk' in url or '.com' in url or '.org' in url

    def find_nth(self, haystack, needle, n):
        parts = haystack.split(needle, n+1)
        if len(parts)<=n+1:
            return -1
        return len(haystack)-len(parts[-1])-len(needle)

    def cut_string(self, url):
        string_cut = self.find_nth(url, '/', 3)
        return url[:string_cut]
