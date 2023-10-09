import requests
from datetime import datetime
import pandas as pd
import os
import psycopg2
from sqlalchemy import create_engine
from dotenv import load_dotenv
from .constants import default_headers



class MainScraper:
    def __init__(self):
        self.sale_name_list = []
        self.auction_date_list = []
        self.auction_time_list = []
        self.default_headers = default_headers

        # Retrieve database credentials from environment variables
        load_dotenv()
        self.db_host = os.getenv("DB_HOST")
        self.db_database = os.getenv("DB_DATABASE")
        self.db_user = os.getenv("DB_USER")
        self.db_password = os.getenv("DB_PASSWORD")

    def date(self, data):
        data = str(data).split('T')
        return data[0]

    def time(self, data):
        data = str(data).split('T')
        time = data[1].replace('Z', '')
        time = datetime.strptime(time, '%H:%M:%S')
        return time.strftime('%I:%M:%S %p')

    def todays_auctions(self):
        auction_url = "https://www.copart.com/public/data/todaysAuctions?appId=g2&copartTimezonePref=%7B%22displayStr%22:%22GMT+5:30%22,%22offset%22:5.5,%22dst%22:false,%22windowsTz%22:%22Asia/Calcutta%22%7D"
        auction_response = requests.get(
            auction_url, headers=self.default_headers)
        response_data = auction_response.json()
        main_data = response_data['data']['saleList']['laterSales']

        for item in main_data:
            sale_name = item['saleName']
            self.sale_name_list.append(sale_name) if sale_name else '-'

            auction_date = item["auctionDateTimeInUTC"]
            self.auction_date_list.append(
                self.date(auction_date)) if auction_date else '-'

            auction_time = auction_date
            self.auction_time_list.append(
                self.time(auction_time)) if auction_time else '-'

    def go(self):
        df = pd.DataFrame({'Sale Name': self.sale_name_list,
                          'Auction Date': self.auction_date_list, 'Auction Time': self.auction_time_list})
        file_name = str(datetime.today()).split(' ')[0]
        file_name = f'{file_name}.csv'

        if os.path.exists(file_name):
            os.remove(file_name)

        df.to_csv(file_name, index=False)

        # Create the connection string using the retrieved credentials
        connection_str = f'postgresql://{self.db_user}:{self.db_password}@{self.db_host}/{self.db_database}'
        db = create_engine(connection_str)

        # Create a connection to the database
        conn = db.connect()

        # Create a connection to PostgreSQL using psycopg2
        connection = psycopg2.connect(
            host=self.db_host,
            database=self.db_database,
            user=self.db_user,
            password=self.db_password,
            port='5432'
        )

        connection.autocommit = True
        cursor = connection.cursor()
        cursor.execute('DROP TABLE IF EXISTS action_table')
        insert_query = '''CREATE TABLE action_table
        (
            SaleName character varying(100),
            AuctionDate date,
            AuctionTime integer
        )  '''
        cursor.execute(insert_query)

        df.to_sql('action_table', conn, if_exists='replace', index=False)
        select_query = '''SELECT * FROM action_table;'''
        cursor.execute(select_query)
        for row in cursor.fetchall():
            print(row)

        # Commit and close the connection
        connection.commit()
        connection.close()


if __name__ == '__main__':
    scraper = MainScraper()
    scraper.todays_auctions()
    scraper.go()
