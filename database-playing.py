import psycopg2

# Connect to an existing database
conn = psycopg2.connect("dbname=testpython")
# do we just do the above on the tests and the db_translator files?

# Open a cursor to perform database operations
cur = conn.cursor()

# Execute a command: this creates a new table
# cur.execute("CREATE TABLE weburls (id serial PRIMARY KEY, weburl varchar(65535));")
# CREATE TABLE weburls (id serial PRIMARY KEY, weburl varchar(65535)); #run in terminal

# Pass data to fill a query placeholders and let Psycopg perform
# the correct conversion (no more SQL injections!)
cur.execute("INSERT INTO weburls (weburl) VALUES (%s)",
        (url,))

# Query the database and obtain data as Python objects
# cur.execute("SELECT * FROM test;")
# cur.fetchone()
# (1, 100, "abc'def")

# Make the changes to the database persistent
conn.commit()

# Close communication with the database
cur.close()
conn.close()

# call the methods at the end
crawler = Crawler()
crawler.crawl('https://www.webpagetest.org/')
