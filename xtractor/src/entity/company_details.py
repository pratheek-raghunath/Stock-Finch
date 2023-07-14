from .base_entity import BaseEntity
from core.database import DatabaseConnection
from psycopg2 import errors

class CompanyDetails(BaseEntity):

    def __init__(self, db: DatabaseConnection, company_details: dict) -> None:
        self.db = db

        self.id = company_details.get('id')
        self.bse = company_details.get('bse')
        self.nse = company_details.get('nse')
        self.series = company_details.get('series')
        self.isin = company_details.get('isin')
        self.company_id = company_details.get('company_id')        
        self.is_deleted = company_details.get('is_deleted')
        self.created_at = company_details.get('created_at')
        self.updated_at = company_details.get('updated_at')

    def save(self):
        UniqueViolation = errors.lookup('23505')

        SQL = """
            INSERT INTO company_details(bse, nse, series, isin, company_id)
            VALUES(%s, %s, %s, %s, %s)
        """
        param = (self.bse, self.nse, self.series, self.isin, self.company_id)
        
        try:
            self.save_to_db(self.db, SQL, param)
        except UniqueViolation:
            self.db.rollback()

        SQL = """
            SELECT * FROM company_details
            WHERE isin=%s
        """
        param = (self.isin,)
        company_details = self.get_row(self.db, SQL, param)
        self.id = company_details[0]
        self.is_deleted = company_details[6]
        self.created_at = company_details[7]
        self.updated_at = company_details[8]
        

