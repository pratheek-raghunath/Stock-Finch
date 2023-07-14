from .base_entity import BaseEntity
from core.database import DatabaseConnection
from psycopg2 import errors

class StockIndex(BaseEntity):

    def __init__(self, db: DatabaseConnection, stock_index: dict) -> None:
        self.db = db

        self.id = stock_index.get('id')
        self.name = stock_index.get('name')
        self.stock_exchange_id = stock_index.get('stock_exchange_id')
        self.is_deleted = stock_index.get('is_deleted')
        self.created_at = stock_index.get('created_at')
        self.updated_at = stock_index.get('updated_at')

    def save(self):
        UniqueViolation = errors.lookup('23505')

        SQL = """
            INSERT INTO stock_index(name, stock_exchange_id)
            VALUES(%s, %s)
        """
        param = (self.name, self.stock_exchange_id)
        
        try:
            self.save_to_db(self.db, SQL, param)
        except UniqueViolation:
            self.db.rollback()

        SQL = """
            SELECT * FROM stock_index
            WHERE name=%s
        """
        param = (self.name,)
        
        stock_index = self.get_row(self.db, SQL, param)
        self.id = stock_index[0]
        self.is_deleted = stock_index[3]
        self.created_at = stock_index[4]
        self.updated_at = stock_index[5]


