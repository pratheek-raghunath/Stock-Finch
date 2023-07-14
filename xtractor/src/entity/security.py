from .base_entity import BaseEntity
from core.database import DatabaseConnection
from psycopg2 import errors

class Security(BaseEntity):

    def __init__(self, db: DatabaseConnection, security: dict) -> None:
        self.db = db

        self.id = security.get('id')
        self.name = security.get('name')
        self.code = security.get('code')
        self.company_id = security.get('company_id')
        self.sector_id = security.get('sector_id')
        self.stock_exchange_id = security.get('stock_exchange_id')
        self.is_deleted = security.get('is_deleted')
        self.created_at = security.get('created_at')
        self.updated_at = security.get('updated_at')

    def save(self):
        UniqueViolation = errors.lookup('23505')

        SQL = """
            INSERT INTO security(name, code, company_id, sector_id, stock_exchange_id)
            VALUES(%s, %s, %s, %s, %s)
        """
        param = (self.name, self.code, self.company_id, self.sector_id, self.stock_exchange_id)
        
        try:
            self.save_to_db(self.db, SQL, param)
        except UniqueViolation:
            self.db.rollback()

        SQL = """
            SELECT * FROM security
            WHERE name=%s
        """
        param = (self.name,)
        security = self.get_row(self.db, SQL, param)
        self.id = security[0]
        self.is_deleted = security[6]
        self.created_at = security[7]
        self.updated_at = security[8]

    def exists(self, security_name):
        SQL = """
            SELECT * FROM security
            WHERE name=%s
        """
    
        param = (security_name,)

        security = self.get_row(self.db, SQL, param)

        if security:
            return True
        else:
            return False

    def get_security_id(self, security_name):
        SQL = """
            SELECT * FROM security
            WHERE name=%s
        """

        param = (security_name,)

        security = self.get_row(self.db, SQL, param)
        
        return security[0]