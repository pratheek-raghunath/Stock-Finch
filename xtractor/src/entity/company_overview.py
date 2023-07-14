from .base_entity import BaseEntity
from core.database import DatabaseConnection
from psycopg2 import errors

class CompanyOverview(BaseEntity):

    def __init__(self, db: DatabaseConnection, company_overview: dict) -> None:
        self.db = db

        self.id = company_overview.get('id')
        self.open = company_overview.get('Open')
        self.previous_close = company_overview.get('Previous Close')
        self.volume  = company_overview.get('Volume')
        self.value = company_overview.get('Value (Lacs)')
        self.vwap = company_overview.get('VWAP')
        self.beta = company_overview.get('Beta')
        self.high = company_overview.get('High')
        self.low = company_overview.get('Low')
        self.uc_limit = company_overview.get('UC Limit')
        self.lc_limit = company_overview.get('LC Limit')
        self._52_week_high = company_overview.get('52 Week High')
        self._52_week_low = company_overview.get('52 Week Low')
        self.ttm_eps = company_overview.get('TTM EPS')
        self.ttm_pe = company_overview.get('TTM PE')
        self.sector_pe = company_overview.get('Sector PE')
        self.book_value_per_share = company_overview.get('Book Value Per Share')
        self.pb = company_overview.get('P/B')
        self.face_value = company_overview.get('Face Value')
        self.market_cap = company_overview.get('Mkt Cap (Rs. Cr.)')
        self.dividend_yeild = company_overview.get('Dividend Yield')
        self._20d_avg_volume = company_overview.get('20D Avg Volume')
        self._20d_avg_volume_percentage = company_overview.get('20D Avg Delivery(%)')
        self.company_id = company_overview.get('company_id')
        self.is_deleted = company_overview.get('is_deleted')
        self.created_at = company_overview.get('created_at')
        self.updated_at = company_overview.get('updated_at')

    def save(self):
        UniqueViolation = errors.lookup('23505')

        SQL = """
            INSERT INTO company_overview(open, previous_close, volume, value, vwap, beta, high, low, uc_limit, lc_limit, _52_week_high, _52_week_low, ttm_eps, ttm_pe, sector_pe, book_value_per_share, pb, face_value, market_cap, dividend_yeild, _20d_avg_volume, _20d_avg_volume_percentage, company_id)
            VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        param = (
            self.open, 
            self.previous_close, 
            self.volume, 
            self.value, 
            self.vwap, 
            self.beta, 
            self.high, 
            self.low, 
            self.uc_limit, 
            self.lc_limit, 
            self._52_week_high, 
            self._52_week_low, 
            self.ttm_eps, 
            self.ttm_pe, 
            self.sector_pe, 
            self.book_value_per_share, 
            self.pb, 
            self.face_value, 
            self.market_cap, 
            self.dividend_yeild, 
            self._20d_avg_volume, 
            self._20d_avg_volume_percentage,
            self.company_id
        )
        
        try:
            self.save_to_db(self.db, SQL, param)
        except UniqueViolation:
            self.db.rollback()

        SQL = """
            SELECT * FROM company_overview
            WHERE company_id=%s
        """
        param = (self.company_id,)
        
        company_overview = self.get_row(self.db, SQL, param)
        self.id = company_overview[0]
        self.is_deleted = company_overview[24]
        self.created_at = company_overview[25]
        self.updated_at = company_overview[26]
        

