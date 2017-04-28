import sqlalchemy
from sqlalchemy import create_engine, select, insert, MetaData, Table

class Translator():
    # replacement for set_environment
    def __init__(self, db = 'postgresql://localhost/beetle_crawler_development'):
        self.database_engine = create_engine(db)
        self.connection = self.database_engine.connect()
        metadata = MetaData()
        self.weburls = Table('weburls', metadata, autoload = True, autoload_with=self.database_engine)



    def write_url(self, url):
        statement = insert(self.weburls).values(weburl = url)
        self.connection.execute(statement)
