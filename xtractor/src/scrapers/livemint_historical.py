#https://www.livemint.com/listing/subsection/market~stock-market-news/1100
#max-cur: 1000

from core.xtractor import BaseExtractor
import time
import core.utils
from entity.stock_news import StockNews

class Livemint(BaseExtractor):

    def __init__(self):
        pass    

    def execute(self, db)-> bool:
        return self.parseLivemint(db)

    def parseLivemint(self, db) -> int:
        #lastcursor=20, max=1000
        start_cursor = 45
        end_cursor = 100

        for cursor in range(start_cursor, end_cursor + 1): 
            domain = 'https://www.livemint.com'
            news_links = []

            stock_news_soup = self.get_soup(f'https://www.livemint.com/listing/subsection/market~stock-market-news/{cursor}')
            news_items = stock_news_soup.find_all(class_='listingNew')

            for news_item in news_items:
                if 'premium' not in news_item['class']:
                    news_links.append(news_item.find('a')['href'])
                    
            for news_link in news_links:
                news_url = domain + news_link
                news_soup = self.get_soup(domain + news_link)

                try:
                    headline = news_soup.find(class_="headline").text
                    description = ''
                    description_p = news_soup.find(class_="contentSec").find_all('p')[:-2]
                    for p_tag in description_p:
                        description += p_tag.text.strip()
                    
                    source = 'Livemint'
                    
                    
                    publish_date_string = news_soup.find(class_='pubtime').text.strip().split('Updated: ')[1][:-4]
                    publish_date = core.utils.get_datetime(publish_date_string, ['%d %b %Y, %H:%M %p'], news_url)
                    image_url = news_soup.find('figure').find('img')['src']
                    
                    news = StockNews(db, headline, description, source, news_url, publish_date, image_url)
                    news.save()
                except (AttributeError, KeyError, TypeError) as inst:
                    raise Exception(f'Site Structure Changed ---  url: {news_link} --- {str(inst)}')
                
                time.sleep(5)

def main():
    Livemint().run()

if __name__ == "__main__":
    main()