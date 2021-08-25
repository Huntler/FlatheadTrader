from feedparser.util import FeedParserDict
from time import struct_time
from typing import List
from datetime import datetime


class News:
    def __init__(self, rss_entry: FeedParserDict = None) -> None:
        if not rss_entry:
            return

        self.hash_id = hash(rss_entry.title)
        self.title = rss_entry.title
        self.tags = []
        if "tags" in rss_entry.keys():
            self.tags = [tag.term for tag in rss_entry.tags]
        self.set_published_date(rss_entry.published_parsed)
        self.set_html_text(rss_entry.content[0].value)

    def set_html_text(self, text) -> None:
        import re
        self.text = re.sub(r"<[^<>]*>", "", text)

    def set_published_date(self, time: struct_time) -> None:
        from datetime import datetime
        from time import mktime

        self.date = datetime.fromtimestamp(mktime(time))

    def to_string(self):
        date = self.date.strftime("%Y-%m-%d %H:%M:%S")
        tags = "; ".join(self.tags)
        return f"Date: {date}\n{tags}\n{self.title}\n{self.text}\n{self.hash_id}"


def create_news(hash_id: int, title: str, text: str, date: datetime, tags: List) -> News:
    news = News()
    news.hash_id = hash_id
    news.title = title
    news.text = text
    news.date = date
    news.tags = tags

    return news
