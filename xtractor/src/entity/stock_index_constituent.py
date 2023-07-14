from .base_entity import BaseEntity
from core.database import DatabaseConnection
from psycopg2 import errors

class StockIndexConstituent(BaseEntity):

    def __init__(self, db: DatabaseConnection, stock_index_constituent: dict) -> None:
        self.db = db

        self.id = stock_index_constituent.get('id')
        self.security_id = stock_index_constituent.get('security_id')
        self.stock_index_id = stock_index_constituent.get('stock_index_id')
        self.is_deleted = stock_index_constituent.get('is_deleted')
        self.created_at = stock_index_constituent.get('created_at')
        self.updated_at = stock_index_constituent.get('updated_at')

    def save(self):
        UniqueViolation = errors.lookup('23505')

        SQL = """
            INSERT INTO stock_index_constituent(security_id, stock_index_id)
            VALUES(%s, %s)
        """
        param = (self.security_id, self.stock_index_id)
        
        try:
            self.save_to_db(self.db, SQL, param)
        except UniqueViolation:
            self.db.rollback()
