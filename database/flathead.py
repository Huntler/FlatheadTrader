from os import stat
from news_scraper.news import News, create_news
import sqlite3
from threading import Lock
from datetime import datetime
from typing import List


class FlatheadData:
    def __init__(self, db_location: str = "flathead.db") -> None:
        self._db_location = db_location
        self._connect()
        self._lock = Lock()

    def _connect(self) -> None:
        self._connection = sqlite3.connect(self._db_location, check_same_thread=False)
        self._c = self._connection.cursor()

    def store_news(self, news: News) -> None:
        # check if the news is already defined in the database
        self._c.execute(
            '''SELECT id FROM News WHERE title=?''', (news.title,))
        n_id = self._c.fetchone()
        if n_id is not None:
            return
        
        with self._lock:

            # insert a news object to the news table
            news_tuple = (news.hash_id, news.title, news.text, news.date.hour,
                        news.date.minute, news.date.second)
            self._c.execute(
                '''INSERT INTO News(hash_id, title, text, hour, minute, second) VALUES(?,?,?,?,?,?)''', news_tuple)
            news_id = self._c.lastrowid

            # insert the related tags
            tags_id = []
            for tag in news.tags:
                self._c.execute('''SELECT id FROM Tag WHERE tag=?''', (tag,))
                t_id = self._c.fetchone()

                if t_id is None:
                    self._c.execute(
                        '''INSERT OR IGNORE INTO Tag(tag) VALUES(?)''', (tag,))
                    tags_id.append(self._c.lastrowid)
                else:
                    tags_id.append(t_id[0])

            # insert the date
            self._c.execute('''SELECT id FROM Date WHERE year=? AND month=? AND day=?''',
                            (news.date.year, news.date.month, news.date.day))
            d_id = self._c.fetchone()

            if d_id is None:
                self._c.execute('''INSERT INTO Date(year, month, day) VALUES(?,?,?)''',
                                (news.date.year, news.date.month, news.date.day))
                date_id = self._c.lastrowid
            else:
                date_id = d_id[0]

            # connect news table to tag and date table
            for tag_id in tags_id:
                self._c.execute(
                    '''INSERT INTO TagsOnNews VALUES(?,?)''', (tag_id, news_id))

            self._c.execute(
                '''INSERT INTO NewsOnDate VALUES(?,?)''', (news_id, date_id))

            # write changes
            self._connection.commit()

    def get_news_by_id(self, val, key: str = "id") -> News:
        # check if the entry refers to a key in News
        if key not in ["id", "hash_id"]:
            return None

        # get from the news table
        statement_news = f'''
        SELECT * FROM News WHERE {key} = {val}
        '''
        self._c.execute(statement_news)
        result_news = self._c.fetchone()

        # get the corresponding date
        statement_date = f'''
        SELECT Date.year, Date.month, Date.day FROM News
        INNER JOIN NewsOnDate ON NewsOnDate.news_id = News.id
        INNER JOIN Date ON Date.id = NewsOnDate.date_id
        WHERE News.{key} = {val}'''
        self._c.execute(statement_date)
        result_date = self._c.fetchone()
        date = datetime(
            result_date[0], result_date[1], result_date[2], result_news[4], result_news[5], result_news[6])

        # get all tags
        statement_tags = f'''
        SELECT Tag.tag FROM News
        INNER JOIN TagsOnNews ON TagsOnNews.news_id = News.id
        INNER JOIN Tag ON Tag.id = TagsOnNews.tag_id
        WHERE News.{key} = {val}
        '''
        self._c.execute(statement_tags)
        result_tags = self._c.fetchall()
        tags = [t[0] for t in result_tags]

        news = create_news(result_news[1], result_news[2],
                           result_news[3], date, tags)
        return news

    def get_news_by_tag(self, tag: str) -> List:
        statement = f'''
        SELECT News.id FROM (SELECT Tag.id, Tag.tag FROM Tag WHERE Tag.tag = "{tag}") AS Tag
        INNER JOIN TagsOnNews ON TagsOnNews.tag_id = Tag.id
        INNER JOIN News ON News.id = TagsOnNews.news_id
        '''

        self._c.execute(statement)
        news = [self.get_news_by_id(i[0]) for i in self._c.fetchall()]
        return news

    def get_news_by_date(self, date: datetime) -> List:
        statement = f'''
        SELECT News.id FROM (SELECT id, year, month, day FROM Date WHERE year={date.year} AND month={date.month} AND day={date.day}) AS Date
        INNER JOIN NewsOnDate ON NewsOnDate.date_id = Date.id
        INNER JOIN News On News.id = NewsOnDate.news_id
        '''

        self._c.execute(statement)
        news = [self.get_news_by_id(i[0]) for i in self._c.fetchall()]
        return news

    def delete_news(self, news: News) -> None:
        # with self._lock:
        #     pass
        pass

    def get_all_tags(self) -> List:
        statement = f'''
        SELECT tag FROM Tag
        '''

        self._c.execute(statement)
        tags = [t[0] for t in self._c.fetchall()]
        return tags


db = FlatheadData()