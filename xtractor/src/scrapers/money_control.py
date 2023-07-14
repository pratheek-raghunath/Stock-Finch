from core.xtractor import BaseExtractor
import re
import time
import core.utils
from entity.stock_news import StockNews

class MoneyControl(BaseExtractor):

    def __init__(self):
        pass    

    def execute(self, db)-> bool:
        return self.parseMoneyControl(db)

    def parseMoneyControl(self, db) -> int: 
        news_links = []
        # news_links_sources = [
        #     'https://www.moneycontrol.com/news/business/',
        #     'https://www.moneycontrol.com/news/business/markets/',
        #     'https://www.moneycontrol.com/news/business/stocks/',
        #     'https://www.moneycontrol.com/news/business/economy/',
        #     'https://www.moneycontrol.com/news/business/companies',
        #     'https://www.moneycontrol.com/news/trends/',
        #     'https://www.moneycontrol.com/news/business/ipo/'
        # ]
        news_links_sources = [
            'https://www.moneycontrol.com/news/business/stocks/',
        ]
        
        for news_link_source in news_links_sources:
            news_links_soup = self.get_soup(news_link_source)
            news_items = news_links_soup.find_all(id=re.compile('^newslist'))
            
            for news_item in news_items:
                if news_item.find(class_='isPremiumCrown'):
                    continue

                url = news_item.find('a')['href']

                if url:
                    if url.startswith('https://www.moneycontrol.com/news/photos'):
                        continue

                    if 'live-updates' in url:
                        continue

                    if 'top-cryptocurrency-news-today' in url:
                        continue

                    if url.startswith('https://www.moneycontrol.com/news/mcminis/'):
                        continue
                    
                    # if url.startswith('https://www.moneycontrol.com/news/business/technicals'):
                    #     continue

                    news_links.append(url)
        
        for news_link in news_links:
            news_soup = self.get_soup(news_link)

            if news_soup.find(class_='ytp-cued-thumbnail-overlay') is not None:
                print('Skipping video')
                continue

            if news_soup.find(class_='top_video_section') is not None:
                print('Skipping video')
                continue
            
            try:
                headline = news_soup.find(class_="artTitle").text

                description = ''
                content_paragraphs = news_soup.find(class_="content_wrapper").find_all('p')
                for content_paragraph in content_paragraphs:
                    description += content_paragraph.text.strip()

                source = 'MoneyControl'

                #publish_date = news_soup.find(class_ = "article_schedule").text.strip()[:-4]
                #publish_date = core.utils.get_datetime(publish_date, ['%B %d, %Y  / %H:%M %p'], news_link)

                publish_div = news_soup.find(class_='tags_last_line')
                publish_date_text = publish_div.text.partition('first published: ')[2]
                publish_date = core.utils.get_datetime(publish_date_text, ['%b %d, %Y %I:%M %p'], news_link)

                if headline == 'Agri Picks Report: Geojit':
                    headline = headline + ' ' + publish_date.strftime('%B %d,%Y')

                if not headline.startswith('Hot Stocks'):
                    image_url = news_soup.find(class_='MC_img')['data-src']
                else:
                    image_url = 'https://images.theabcdn.com/i/38791461.jpg'
            
                news = StockNews(db, headline, description, source, news_link, publish_date, image_url)
                news.save()
                
            except (AttributeError, KeyError, TypeError) as inst:
                raise Exception(f'Site Structure Changed ---  url: {news_link} --- {str(inst)}')
            time.sleep(5)
    

def main():
    MoneyControl().run()

if __name__ == "__main__":
    main()