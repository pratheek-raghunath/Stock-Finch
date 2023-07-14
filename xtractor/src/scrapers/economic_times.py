from core.xtractor import BaseExtractor
import time
import core.utils
from entity.stock_news import StockNews

class EconomicTimes(BaseExtractor):

    def __init__(self):
        pass    

    def execute(self, db)-> bool:
        return self.parseEconomicTimes(db)

    def parseEconomicTimes(self, db) -> int: 
        news_links = []

        stock_news_soup = self.get_soup('https://economictimes.indiatimes.com/markets/stocks/news')
        news_items = stock_news_soup.find_all(class_='eachStory')
        
        for news_item in news_items:
            news_links.append('https://economictimes.indiatimes.com' + news_item.find('a')['href'])

        for news_link in news_links:
            if "videoshow" in news_link or "slideshow" in news_link:
                continue 

            news_soup = self.get_soup(news_link)
            
            try:
                try:
                    publish_date = ''.join(news_soup.find('time').text.split()[2:-1])
                    publish_date = core.utils.get_datetime(publish_date, ['%b%d,%Y,%I:%M%p'], news_link)
                except Exception:
                    print('Paywall')
                    continue

                headline = news_soup.find(class_="artTitle").text
                
                description = news_soup.find(class_="artText").text.strip()
                source = 'The Economic Times'

                publish_date = ''.join(news_soup.find('time').text.split()[2:-1])
                publish_date = core.utils.get_datetime(publish_date, ['%b%d,%Y,%I:%M%p'], news_link)
                
                image_url = news_soup.find(class_='artImg').find('img')['src']
                
                news = StockNews(db, headline, description, source, news_link, publish_date, image_url)
                news.save()
            except (AttributeError, KeyError, TypeError) as inst:
                raise Exception(f'Site Structure Changed ---  url: {news_link} --- {str(inst)}')

            time.sleep(5)
    

def main():
    EconomicTimes().run()

if __name__ == "__main__":
    main()