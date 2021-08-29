import sqlite3
from sqlite3.dbapi2 import connect

connection = sqlite3.connect("flathead.db")
c = connection.cursor()

c.execute(
    '''
    CREATE TABLE News([id] INTEGER PRIMARY KEY AUTOINCREMENT, [hash_id] INTEGER UNIQUE, [title] TEXT, [text] TEXT, 
    [hour] INTEGER, [minute] INTEGER, [second] INTEGER)
    '''
)

c.execute(
    '''
    CREATE TABLE Date([id] INTEGER PRIMARY KEY AUTOINCREMENT, [year] INTEGER, [month] INTEGER, [day] INTEGER)
    '''
)

c.execute(
    '''
    CREATE TABLE Tag([id] INTEGER PRIMARY KEY AUTOINCREMENT, [tag] TEXT UNIQUE)
    '''
)

c.execute(
    '''
    CREATE TABLE NewsOnDate([news_id] INTEGER, [date_id] INTEGER)
    '''
)

c.execute(
    '''
    CREATE TABLE TagsOnNews([tag_id] INTEGER, [news_id] INTEGER)
    '''
)

c.execute(
    '''
    CREATE TABLE FeedSource([id] INTEGER PRIMARY KEY AUTOINCREMENT, [name] TEXT, [url] TEXT UNIQUE)
    '''
)

c.execute(
    '''
    CREATE TABLE NewsOnFeedSource([news_id] INTEGER, [feed_source_id] INTEGER)
    '''
)


connection.commit()