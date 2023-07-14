from core.database import DatabaseConnection

class BaseEntity:  
    def __init__(self) -> None:
        pass

    def save_to_db(self, dbcon: DatabaseConnection, sql: str, parameter: tuple) -> None:
        dbcon.cursor.execute(sql, parameter)
        dbcon.commit()

    def get_row(self, dbcon: DatabaseConnection, sql: str, parameter: tuple):
        dbcon.cursor.execute(sql, parameter)
        return dbcon.cursor.fetchone()
    