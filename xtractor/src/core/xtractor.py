import psycopg2
import requests
import time
from .database import DatabaseConnection
from .log import DatabaseLog
from abc import ABC, abstractmethod
from bs4 import BeautifulSoup

class BaseExtractor(ABC):
    @abstractmethod
    def execute(self) -> bool:
        raise Exception("Function execute is not Implemented")

    def run(self):
        scrapperName: str = self.getScrapperName()
        try:
            dbcon = DatabaseConnection()
            dblog = DatabaseLog(scrapperName, dbcon)
            
            self.execute(dbcon) 
            print("Xtractor ran successfully for site: {name}".format(name=scrapperName))
            dblog.set_runner_status('SUCCESS')
        except psycopg2.Error as pe:
            dbcon.rollback()
            print(f'Database error:\npgcode: {pe.pgcode}\npgerror: {pe.pgerror}')
            raise pe
        except Exception as inst:
            print("Xtractor failed to run successfully for : {name}".format(name=scrapperName))
            dblog.log_message('FAILED', str(inst))
            dblog.set_runner_status('FAILED')
            raise inst
        finally:
            dbcon.close()

    def getScrapperName(self):
        return self.__class__.__name__

    def get_page(self, url: str) -> requests.models.Response:
        num_retries = 3

        for i in range(num_retries):
            try:
                page = requests.get(url)
                page.raise_for_status()
            except requests.HTTPError() as e:
                raise e
            except requests.RequestException as e:
                if i == num_retries - 1:
                    raise e
                else:
                    time.sleep(10)
            else:
                return page

    def get_soup(self, url: str) -> BeautifulSoup:
        print('Scraping: ' + url)
        page = self.get_page(url)

        soup = BeautifulSoup(page.text, 'lxml')
        return soup


    