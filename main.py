from datetime import date, datetime
from os import stat
import sqlite3
from typing import List, Tuple
import feedparser
from feedparser.util import FeedParserDict

from news_scraper.news import News, create_news
from database.flathead import FlatheadData

# get current news using RSS feed
newsfeed = feedparser.parse(
    "http://www.stern.de/feed/standard/alle-nachrichten/")
news = [News(rss_entry=entry) for entry in newsfeed.entries]

db = FlatheadData()

# only news that are not stored are saved
for n in news:
    db.store_news(news=n)

# testing a bit
a_date = datetime(2021, 8, 25)
newsofdate = db.get_news_by_date(date=a_date)
print(f"Amount of news, {a_date.strftime('%Y-%m-%d')}: {len(newsofdate)}")
print()

tag = "CDU"
print(f"'{tag}' related news on dates")
newsoftag = db.get_news_by_tag(tag=tag)
for n in newsoftag:
    print("\t", n.date.strftime('%Y-%m-%d'))
print()

# Outputs:
#
# Amount of news, 2021-08-25: 20
#
# 'CDU' related news on dates
#          2021-08-25
#          2021-08-25