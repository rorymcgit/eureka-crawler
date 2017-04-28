import sqlalchemy
from sqlalchemy import create_engine, select, insert, MetaData, Table

class Translator():
    # replacement for set_environment
    def __init__(self, db = 'postgresql://localhost/beetle_crawler_development'):
        self.database_engine = create_engine(db)
        self.connection = self.database_engine.connect()
        metadata = MetaData()
        self.weburls = Table('weburls', metadata, autoload = True, autoload_with=self.database_engine)
        self.weburlsandcontent = Table('weburlsandcontent', metadata, autoload = True, autoload_with=self.database_engine)

    def write_url(self, url):
        statement = insert(self.weburls).values(weburl = url)
        self.connection.execute(statement)


    # def write_urls_and_content(self, url, title, description, keywords):
    #     self.database_cursor.execute("INSERT INTO weburlsandcontent (weburl, title, description, keywords) VALUES (%s, %s, %s, %s)",
    #             (url, title, description, keywords,))
    #     self.database.commit()
    #
    def prepare_urls_for_writing_to_db(self, weburls_array):
        for url in weburls_array:
            if self.get_database_size() < 1000:
                self.write_url(url)
            else:
                raise Exception

    def get_database_size(self):
        select_all = select([self.weburls])
        results = self.connection.execute(select_all)
        return results.rowcount
    #     self.database_cursor.execute("SELECT * FROM weburls;")
    #     return self.database_cursor.rowcount
