from .database import DatabaseConnection

class DatabaseLog:
    
    def __init__(self, extractor_name: str, dbcon: DatabaseConnection) -> None:
        self.extractor_name = extractor_name
        self.dbcon = dbcon

        self.runner_id = self.setup_runner()

    def setup_runner(self) -> int:
        cur = self.dbcon.cursor

        cur.execute(
            "INSERT INTO runners(extractor_name, start_date, status) VALUES(%s, NOW(), 'RUNNING') RETURNING id", 
            (self.extractor_name,)
            )

        runner_id = cur.fetchone()[0]
        
        self.dbcon.commit()

        return runner_id

    def set_runner_status(self, status: str) -> None:
        cur = self.dbcon.cursor

        cur.execute(
                "UPDATE runners SET end_date=NOW(), status=%s WHERE id=%s", 
                (status, self.runner_id)
            )
          
        self.dbcon.commit()

    def log_message(self, severity: str, message: str) -> None:
        cur = self.dbcon.cursor

        cur.execute(
            "INSERT INTO logs(runner_id, extractor_name, log_date, severity, message) VALUES(%s, %s, NOW(), %s, %s)",
            (self.runner_id, self.extractor_name, severity, message)
        )

        self.dbcon.commit()