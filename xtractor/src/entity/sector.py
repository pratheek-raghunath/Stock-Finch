from .base_entity import BaseEntity
from core.database import DatabaseConnection
from psycopg2 import errors

class Sector(BaseEntity):

    def __init__(self, db: DatabaseConnection, sector: dict) -> None:
        self.db = db

        self.id = sector.get('id')
        self.name = sector.get('name')
        self.is_deleted = sector.get('is_deleted')
        self.created_at = sector.get('created_at')
        self.updated_at = sector.get('updated_at')

    def save(self):
        UniqueViolation = errors.lookup('23505')

        SQL = """
            INSERT INTO sector(name)
            VALUES(%s)
        """
        param = (self.name,)
        
        try:
            self.save_to_db(self.db, SQL, param)
        except UniqueViolation:
            self.db.rollback()

        SQL = """
            SELECT * FROM sector
            WHERE name=%s
        """
        param = (self.name,)
        
        sector = self.get_row(self.db, SQL, param)
        self.id = sector[0]
        self.is_deleted = sector[2]
        self.created_at = sector[3]
        self.updated_at = sector[4]
        

