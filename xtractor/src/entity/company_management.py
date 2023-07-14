from .base_entity import BaseEntity
from core.database import DatabaseConnection
from psycopg2 import errors

class CompanyManagement(BaseEntity):

    def __init__(self, db: DatabaseConnection, company_management: dict) -> None:
        self.db = db

        self.id = company_management.get('id')
        self.name = company_management.get('name')
        self.designation = company_management.get('designation')
        self.company_id = company_management.get('company_id')        
        self.is_deleted = company_management.get('is_deleted')
        self.created_at = company_management.get('created_at')
        self.updated_at = company_management.get('updated_at')

    def save(self):
        UniqueViolation = errors.lookup('23505')

        SQL = """
            INSERT INTO company_management(name, designation, company_id)
            VALUES(%s, %s, %s)
        """
        param = (self.name, self.designation, self.company_id)
        
        try:
            self.save_to_db(self.db, SQL, param)
        except UniqueViolation:
            self.db.rollback()

        SQL = """
            SELECT * FROM company_management
            WHERE name=%s AND designation=%s AND company_id=%s
        """
        param = (self.name, self.designation, self.company_id)
        
        company_management = self.get_row(self.db, SQL, param)
        self.id = company_management[0]
        self.is_deleted = company_management[4]
        self.created_at = company_management[5]
        self.updated_at = company_management[6]
        

