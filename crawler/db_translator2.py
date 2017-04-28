import sqlalchemy
from sqlalchemy import create_engine

class Translator():
    # replacement for set_environment
    def __init__(self, db = 'postgresql://localhost/beetle_crawler_development'):
        "hello"
