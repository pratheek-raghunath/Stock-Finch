from core.xtractor import BaseExtractor
import re
import time
import core.utils
from entity.news import News

class MoneyControl(BaseExtractor):

    def __init__(self):
        pass    

    def execute(self, db)-> bool:
        return self.parseMoneyControl(db)

    def parseMoneyControl(self, db) -> int: 
        news_links = []

        stock_news_soup = self.get_soup('https://www.moneycontrol.com/news/business/stocks')
        news_items = stock_news_soup.find_all(id=re.compile('^newslist'))
        
        for news_item in news_items:
            if news_item.find(class_='isPremiumCrown'):
                continue

            url = news_item.find('a')['href']

            if url:
                if url.startswith('https://www.moneycontrol.com/news/photos'):
                    continue

                news_links.append(url)

        for news_link in news_links:
            news_soup = self.get_soup(news_link)
            
            try:
                headline = news_soup.find(class_="artTitle").text

                description = ''
                content_paragraphs = news_soup.find(class_="content_wrapper").find_all('p')
                for content_paragraph in content_paragraphs:
                    description += content_paragraph.text.strip()

                source = 'MoneyControl'

                publish_date = news_soup.find(class_ = "article_schedule").text.strip()[:-4]
                publish_date = core.utils.get_datetime(publish_date, ['%B %d, %Y  / %H:%M %p'], news_link)

                if headline == 'Agri Picks Report: Geojit':
                    headline = headline + ' ' + publish_date.strftime('%B %d,%Y')

                if not headline.startswith('Hot Stocks'):
                    image_url = news_soup.find(class_='MC_img')['data-src']
                else:
                    image_url = 'https://images.theabcdn.com/i/38791461.jpg'
            
                news = News(db, headline, description, source, news_link, publish_date, image_url)
                news.save()
                
            except (AttributeError, KeyError, TypeError) as inst:
                raise Exception(f'Site Structure Changed ---  url: {news_link} --- {str(inst)}')
            time.sleep(5)
    

def main():
    MoneyControl().run()

if __name__ == "__main__":
    main()