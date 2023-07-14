from .base_entity import BaseEntity
from core.database import DatabaseConnection
from psycopg2 import errors

class Company(BaseEntity):

    def __init__(self, db: DatabaseConnection, company: dict) -> None:
        self.db = db

        self.id = company.get('id')
        self.name = company.get('name')
        self.date_of_listing = company.get('date_of_listing')
        self.is_deleted = company.get('is_deleted')
        self.created_at = company.get('created_at')
        self.updated_at = company.get('updated_at')

    def save(self):
        UniqueViolation = errors.lookup('23505')

        SQL = """
            INSERT INTO company(name, date_of_listing)
            VALUES(%s, %s)
        """
        param = (self.name, self.date_of_listing)
        
        try:
            self.save_to_db(self.db, SQL, param)
        except UniqueViolation:
            self.db.rollback()

        SQL = """
            SELECT * FROM company
            WHERE name=%s
        """
        param = (self.name,)
        
        company = self.get_row(self.db, SQL, param)
        self.id = company[0]
        self.is_deleted = company[3]
        self.created_at = company[4]
        self.updated_at = company[5]
        

