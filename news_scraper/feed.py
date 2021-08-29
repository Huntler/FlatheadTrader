from news_scraper.news import News
from database.flathead import db
from threading import Thread
import feedparser
import time


class Feed:
    def __init__(self, name: str, url: str, update_interval: int = 900, verbose: bool = True) -> None:
        self._url = url
        self._update_interval = update_interval
        self._verbose = verbose
        self._name = name
        self._service_running = True

        self._background_thread = Thread(target=Feed.run_service, args=(self,), daemon=True)
        self._background_thread.start()

    def stop(self):
        self._service_running = False

    @staticmethod
    def run_service(feed):
        while feed._service_running:
            newsfeed = feedparser.parse(feed._url)
            news = [News(rss_entry=entry) for entry in newsfeed.entries]

            if feed._verbose:
                print(f"Feed service '{feed._name}' fetched {len(news)} news.")

            for n in news:
                db.store_news(news=n)

            time.sleep(feed._update_interval)
