

from abc import ABC, abstractmethod

class BaseEntity:  
    def __init__(self) -> None:
        pass

    def save_to_db(self, dbcon, sql, parameter):
        dbcon.cursor.execute(sql, parameter)
        dbcon.commit()
    
