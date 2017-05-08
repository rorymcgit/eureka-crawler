# Eureka Web Crawler


Final project (weeks 11 & 12) at Makers Academy. Tasked with working on a project of our choice in languages and testing frameworks of our choice.

Team:
- [Clem Capel-Bird](https://github.com/ClemCB)
- [Nicholas Leacock](https://github.com/marudine)
- [Vicky Ledsom](https://github.com/ledleds)
- [Rory McGuinness](https://github.com/rorymcgit)

## Installation

- Clone this repo

To create your test and development databases with required tables:
- Run `./db-config.sh`. *If you get an error regarding permissions, you'll need to run ```chmod +x db-config.sh```, and then run ```./db-config.sh``` again.*
- To run all tests `python3 -m unittest discover -s test -p "*_tests.py"`

To crawl:
- Open ./initiate_crawl.py
- Set desired database limit
- Enter a website to begin crawling
- Run `python3 initiate_crawl.py`

## Technologies

- Python3
- BeautifulSoup4 (HTML parsing)
- PyUnit (testing framework)
- MagicMock (test doubles)
- PostgreSQL
- SQLAlchemy
