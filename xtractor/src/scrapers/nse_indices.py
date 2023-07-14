from core.xtractor import BaseExtractor
from core.database import DatabaseConnection
from entity.stock_index import StockIndex
from entity.company import Company
from entity.sector import Sector
from entity.security import Security
from entity.company_details import CompanyDetails
from entity.company_management import CompanyManagement
from entity.company_overview import CompanyOverview
from entity.stock_index_constituent import StockIndexConstituent
import time

class NseIndices(BaseExtractor):

    def __init__(self):
        self.db = None
        self.domain = 'https://www.moneycontrol.com'
    
    def execute(self, db: DatabaseConnection) -> bool:
        self.db = db
        return self.parseNseIndices()

    def parseNseIndices(self) -> bool:
        nse_soup = self.get_soup('https://www.moneycontrol.com/markets/indian-indices/market-terminal?deviceType=web&indicesName=demo&indicesId=7&exName=N&subSelectedTabOT=d&subSelectedTabOPL=cl&classic=true')
        nse_ul = nse_soup.find('ul', {'class': 'ntlist'})
        #for debugging:
        # self.parseNseIndex('NIFTY 500', '7') 
        # return
        for nse_li in nse_ul.find_all('li'):
            nse_a = nse_li.find('a')
            self.parseNseIndex(nse_a.text.strip(), nse_li['data-subid'])
            time.sleep(5)

    def parseNseIndex(self, index_name, index_data_sub_id):
        stock_index_dict = {'name': index_name, 'stock_exchange_id': 1}
        stock_index = StockIndex(self.db, stock_index_dict)
        stock_index.save()

        stock_index_soup = self.get_soup('https://www.moneycontrol.com/markets/indian-indices/changeTableData?deviceType=web&exName=N&indicesID=' + index_data_sub_id + '&selTab=o&subTabOT=d&subTabOPL=cl&selPage=marketTerminal&classic=true')

        if stock_index_soup.text.strip() == 'No Data Available':
            return
        
        stock_index_table = stock_index_soup.find('table', {'id': 'indicesTable'})
        #for debugging
        # self.parseCompany(stock_index, 'SBI', 'https://www.moneycontrol.com/india/stockpricequote/banks-public-sector/statebankindia/SBI') 
        # return
        for stock_index_company_a_tag in stock_index_table.find_all('a'):
            if stock_index_company_a_tag['href'] == 'https://www.moneycontrol.com/india/stockpricequote//hemispherepropertiesindia/HPI01':
                print('\n\nSkipping HEMISPHERE\n\n')
                continue
            
            if 'zydus' in stock_index_company_a_tag['href']:
                print('\n\nSkipping Zydus\n\n')
                continue

            if not Security(self.db, {}).exists(stock_index_company_a_tag.text):
                self.parseCompany(stock_index, stock_index_company_a_tag.text, stock_index_company_a_tag['href'])
                time.sleep(5)
            else:
                print('Skipping security: ' + stock_index_company_a_tag.text)

            security_id = Security(self.db, {}).get_security_id(stock_index_company_a_tag.text)
            stock_index_constituent_dict = {
                'security_id': security_id,
                'stock_index_id': stock_index.id
            }
            stock_index_constituent = StockIndexConstituent(self.db, stock_index_constituent_dict)
            stock_index_constituent.save()
            
    def parseCompany(self, stock_index, security_name, company_url):
        company_soup = self.get_soup(company_url)

        company_details_dict = self.get_company_details(company_soup)
                
        company_name = self.get_company_name(company_soup)
        company = Company(self.db, company_name)
        company.save()

        sector_name = self.get_sector_name(company_soup)
        sector = Sector(self.db, sector_name)
        sector.save()

        security_dict = {
            'name': security_name,
            'code': company_details_dict['isin'],
            'company_id': company.id,
            'sector_id': sector.id,
            'stock_exchange_id': 1,
        }
        security = Security(self.db, security_dict)
        security.save()

        company_details_dict['company_id'] = company.id
        company_details = CompanyDetails(self.db, company_details_dict)
        company_details.save()

        company_management_list = self.get_company_management(company_soup, company.id)
        for company_manager in company_management_list:
            company_management = CompanyManagement(self.db, company_manager)
            company_management.save()

        company_overview_dict = self.get_company_overview(company_soup)
        company_overview_dict['company_id'] = company.id
        company_overview = CompanyOverview(self.db, company_overview_dict)
        company_overview.save()
        
    def get_company_name(self, security_soup):
        elem = security_soup.find("h1")
        return {"name": elem.text}

    def get_sector_name(self, security_soup):
        elem = security_soup.find(id = "stockName")
        elem.text.split('\n')
        sector = elem.text.strip().split('\n')[4].strip()
        return {"name": sector}

    def get_company_overview(self, security_soup):
        tables_div = security_soup.find(id= "stk_overview")
        tables = tables_div.find_all(class_ = "oview_table")
        overview = {}
        for table in tables[:4]:
            for table_row in table.find_all('tr'):
                table_data = table_row.find_all('td')
                key = table_data[0].text.strip()
                value =table_data[1].text.strip().replace(',','')

                if key == 'i\n\n\xa0VWAP':
                    key = 'VWAP'

                if key == 'Beta':
                    value = table_data[1].find(class_='nsebeta').text
                
                overview[key] = value

        for key in overview:
            try:
                to_float = float(overview[key])
            except ValueError:
                overview[key] = '0.0'

        return overview    

    def get_company_details(self, security_soup):
        det = security_soup.find(class_ = "comp_inf")
        elem = det.find_all("li",class_ = "clearfix")
        details = {}
        for i in range(len(elem)-4,len(elem)):
            j=0
            details[elem[i].text.strip().split('\n')[j].lower().replace(':','')] = elem[i].text.strip().split('\n')[j+1]
        return details


    def get_company_management(self, security_soup, company_id):
        mgmt = security_soup.find(class_ = "comp_inf")
        elem = mgmt.find_all("li")
        management = []
        temp = elem[17].text.strip().split('\n')
        while("" in temp):
            temp.remove("")
        for i in range(1,len(temp)-1,2):
            person = {}
            person['name'] = temp[i].strip()
            person['designation'] = temp[i+1].strip()
            person['company_id'] = company_id
            management.append(person)
        return management
    
def main():
    NseIndices().run()

if __name__ == "__main__":
    main()