# Eureka Web Crawler


This is a Makers Academy final project. We were tasked with working on a project of our choice in languages, testing frameworks and technologies of our choice over the course of 11 days.

We chose to build a search engine, writing the crawler in Python and the [query engine](https://github.com/rorymcgit/eureka-search) in Node.js.

Central throughout the project were TDD/BDD, XP values and agile practices. We used a Kanban workflow to manage the project's progression.

On our latest crawl, the program visited over 28'000 webpages, filtering content down to 4'600 high-quality searchable results.

Team:
- [Clem Capel-Bird](https://github.com/ClemCB)
- [Nicholas Leacock](https://github.com/marudine)
- [Vicky Ledsom](https://github.com/ledleds)
- [Rory McGuinness](https://github.com/rorymcgit)

## Installation

- Clone this repo
- If you don't already have Python 3 installed run `brew install python3`
- Run `pip3 install -r requirements.txt` to install dependencies

To create your test and development databases with required tables:
- Run `./db-config.sh`. *If a permissions error is returned, you'll need to run ```chmod +x db-config.sh```, and then run ```./db-config.sh``` again.*
- To run all tests `python3 -m unittest discover -s test -p "*_tests.py"`

To crawl:
- Open ./initiate_crawl.py
- Set desired database limit
- Enter a website to begin crawling, or use a local HTML file with a list of links, as is the example
- Run `python3 initiate_crawl.py`

## Technologies

- Python3
- PyUnit (testing framework)
- MagicMock (test doubles)
- BeautifulSoup4 (HTML parsing)
- PostgreSQL
- SQLAlchemy
