import requests
from core.xtractor import BaseExtractor
from bs4 import BeautifulSoup
from entity.base_entity import BaseEntity

from entity.stockindex import StockIndex



class MasterDataXtractor(BaseExtractor):    
    
    def __init__(self):          
        self.dbcon = None 

    def execute(self, db)-> bool:
        self.dbcon = db
        return self.parseIndexData()
    
    def parseIndexData(self):
        entity = BaseEntity() 
        SQL = '''INSERT INTO stock_index(name, stock_exchange_id, is_deleted)
             VALUES(%s, %s, %s)'''
        URL = 'https://www.moneycontrol.com/markets/indian-indices/'
        response = requests.get(URL).text
        soup = BeautifulSoup(response, 'html.parser')
        ul = soup.find("ul", {"class": "ntlist"})
        for li in ul.find_all('li'):
            index_name = li.h2.a.text
            print(index_name, '\t', li.h2.a['href'])
            param = (index_name, 1, False)
            entity.save_to_db(self.dbcon, SQL, param)
        


def main():
    MasterDataXtractor().run()

if __name__ == "__main__":
    main()
