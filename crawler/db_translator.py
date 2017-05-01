import sqlalchemy
from sqlalchemy import create_engine, select, insert, MetaData, Table

class Translator():
    def __init__(self, db = 'postgresql://localhost/beetle_crawler_development'):
        self.database_engine = create_engine(db)
        self.connection = self.database_engine.connect()
        metadata = MetaData()
        self.weburls = Table('weburls', metadata, autoload = True, autoload_with = self.database_engine)
        self.weburlsandcontent = Table('weburlsandcontent', metadata, autoload = True, autoload_with = self.database_engine)
        self.database_limit = 1000
        self.current_id = 1

    def write_url(self, url):
        if self.url_checker(url):
            url = self.cut_string(url)
            statement = insert(self.weburls).values(weburl = url)
            self.connection.execute(statement)

    def write_urls_and_content(self, url, title, description, keywords):
        statement = insert(self.weburlsandcontent).values(weburl = url, title = title, description = description, keywords = keywords)
        self.connection.execute(statement)
        self.current_id += 1

    def prepare_urls_for_writing_to_db(self, weburls):
        for url in weburls:
            if self.get_weburls_table_size() < self.database_limit:
                self.write_url(url)
            else:
                return 'weburls is now full'
                # raise Exception

    def get_weburls_table_size(self):
        select_all = select([self.weburls])
        return self.connection.execute(select_all).rowcount

    def get_weburls_and_content_table_size(self):
        select_all = select([self.weburlsandcontent])
        return self.connection.execute(select_all).rowcount

    def get_next_url(self):
        my_url = select([self.weburls]).where(self.weburls.c.id == self.current_id)
        return self.connection.execute(my_url).fetchone()['weburl']

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
        if url.count('/') >= 4:
            string_cut = self.find_nth(url, '/', 3)
            return url[:string_cut]
        else:
            return url
