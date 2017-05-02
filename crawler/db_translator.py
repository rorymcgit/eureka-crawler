import sqlalchemy
from sqlalchemy import create_engine, select, insert, MetaData, Table
from sqlalchemy.orm import sessionmaker


class Translator():
    def __init__(self, db = 'postgresql://localhost/beetle_crawler_development', database_limit = 1000):
        database_engine = create_engine(db)
        self.connection = database_engine.connect()
        metadata = MetaData()
        self.weburls = Table('weburls', metadata, autoload = True, autoload_with = database_engine)
        self.weburlsandcontent = Table('weburlsandcontent', metadata, autoload = True, autoload_with = database_engine)
        self.database_limit = database_limit
        self.current_id = 1

    def write_url(self, url):
        if self.get_weburls_table_size() < self.database_limit:
            if self.url_checker(url):
                url = self.cut_string(url)
                if not self.url_is_in_database(url):
                    statement = insert(self.weburls).values(weburl = url)
                    self.connection.execute(statement)
        else:
            return "Weburls table is full"

    def write_urls_and_content(self, url, title, description, keywords):
        statement = insert(self.weburlsandcontent).values(weburl = url, title = title, description = description, keywords = keywords)
        self.connection.execute(statement)

    def prepare_urls_for_writing_to_db(self, weburls):
        for url in weburls:
            self.write_url(url)

    def get_weburls_table_size(self):
        select_all = select([self.weburls])
        return self.connection.execute(select_all).rowcount

    def get_weburls_and_content_table_size(self):
        select_all = select([self.weburlsandcontent])
        return self.connection.execute(select_all).rowcount

    def both_tables_are_not_full_yet(self):
        return self.get_weburls_table_size() < self.database_limit or self.get_weburls_and_content_table_size() < self.database_limit

    def get_next_url(self):
        self.current_id += 1
        next_url = select([self.weburls]).where(self.weburls.c.id == self.current_id)
        return self.connection.execute(next_url).fetchone()['weburl']

    def url_is_in_database(self, url):
        select_statement = self.weburls.select(self.weburls.c.weburl == url)
        res_proxy = self.connection.execute(select_statement)
        results = [item[1] for item in res_proxy.fetchall()]
        return len(results)

    def url_checker(self, url):
        return self.check_url_beginning(url) and self.check_url_domain(url) and not self.is_low_quality_link(url)

    def check_url_beginning(self, url):
        return url.startswith('http')

    def check_url_domain(self, url):
        return '.co.uk' in url or '.com' in url or '.org' in url

    def is_low_quality_link(self, url):
        low_quality_links = ['plus.google.com', 'accounts.google.com', 'facebook.com', 'twitter.com', 'apple.com', 'instagram.com', 'download-sha1', 'download.mozilla', 'donate.mozilla', 'bugzilla']
        return True if any(bad_link in url for bad_link in low_quality_links) else False

    def find_nth(self, haystack, needle, n):
        parts = haystack.split(needle, n+1)
        if len(parts)<=n+1:
            return -1
        return len(haystack)-len(parts[-1])-len(needle)

    def full_database_message(self):
        return "The database is full."

    def cut_string(self, url):
        if url.count('/') >= 4:
            string_cut = self.find_nth(url, '/', 3)
            return url[:string_cut]
        else:
            return url
