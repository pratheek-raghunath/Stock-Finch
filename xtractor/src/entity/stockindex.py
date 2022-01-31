from bs4 import StopParsing

from entity.base_entity import BaseEntity


class StockIndex(BaseEntity):
    def __init__(self) -> None:
        self.index_name = None
        self.exchange_id = None
        self.is_deleted = False
    
    def save(self):
        SQL = '''INSERT INTO stock_index(name, stock_exchange_id)
             VALUES(%s, %s)'''
        params = ()
    
    
    
        
        


