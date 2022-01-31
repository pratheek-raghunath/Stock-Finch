import psycopg2
import os

class DatabaseConnection:
    def __init__(self) -> None:
        self.dbcon = self.connect()
        self.cursor = self.dbcon.cursor()         
        
    def connect(self):
        # DB_PASSWORD = os.environ['POSTGRES_PASSWORD']
        # DB_USER = os.environ['POSTGRES_USER']
        # POSTGRES_DB = os.environ['POSTGRES_DB']
        # self.dbcon = psycopg2.connect(user=DB_USER, password=DB_PASSWORD,
        #                             database=POSTGRES_DB, host='postgresql')    
        DB_PASSWORD = 'x8Fpkla2CRb46MiCi467rp6Himr-D_VB'
        DB_USER = 'davqufbg'
        POSTGRES_DB = 'davqufbg'
        DB_HOST = 'john.db.elephantsql.com'
        self.dbcon = psycopg2.connect(user=DB_USER, password=DB_PASSWORD,
                                    database=POSTGRES_DB, host=DB_HOST)                        
        return self.dbcon
    

    def close(self):
        self.dbcon.close()
    
    def test(self):
        self.cur = self.cursor
        values = self.cur.execute('SELECT CURRENT_TIMESTAMP')
        print("++++++CURRENT_TIMESTAMP+++++++++++++++",self.cur.fetchall())
        self.dbcon.close()

    def commit(self):
        self.dbcon.commit()

    def rollback(self):
        self.dbcon.rollback()

