from .base_entity import BaseEntity
from datetime import datetime 
from psycopg2 import errors

class News(BaseEntity):

    def __init__(self, dbcon, headline: str, description: str, source: str, news_link: str, publish_date: str, image_url: str) -> None:
        self.dbcon = dbcon
        self.headline = headline
        self.description = description 
        self.source = source 
        self.news_link = news_link 
        self.publish_date = publish_date
        self.image_url = image_url
    
    def save(self):
        UniqueViolation = errors.lookup('23505')

        SQL = '''INSERT INTO stock_news(headline, description, source, news_link, publish_date, image_url)
            VALUES(%s, %s, %s, %s, %s, %s)'''

        param = (self.headline, self.description, self.source, self.news_link, self.publish_date, self.image_url)
        
        try:
            self.save_to_db(self.dbcon, SQL, param)
        except UniqueViolation:
            self.dbcon.rollback()