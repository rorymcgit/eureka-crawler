import psycopg2


class Translator():
    def set_environment(self):
        conn = psycopg2.connect("dbname=beetle_crawler_development")
        cur = conn.cursor()
