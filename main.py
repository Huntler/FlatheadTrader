from datetime import datetime
import time

from news_scraper.feed import Feed
from database.flathead import db

# get current news using RSS feed
stern_feed = Feed(name="stern", url="http://www.stern.de/feed/standard/alle-nachrichten/", update_interval=5)
spiegel_feed = Feed(name="spiegel", url="https://www.spiegel.de/schlagzeilen/index.rss", update_interval=3)

# testing a bit
a_date = datetime(2021, 8, 29)
newsofdate = db.get_news_by_date(date=a_date)
print(f"Amount of news, {a_date.strftime('%Y-%m-%d')}: {len(newsofdate)}")
print()

time.sleep(6)
# tags = db.get_all_tags()
# print("; ".join(tags))

tag = "Deals des Tages"
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