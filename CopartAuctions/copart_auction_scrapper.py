import requests
from datetime import datetime
import pandas as pd
import os
import psycopg2
from sqlalchemy import create_engine
from dotenv import load_dotenv
from logs import Logger
import config
import json


class MainScraper:
    data_list = list()
    default_headers = None
    logger = Logger('Copart_Auction').log_obj

    @classmethod
    def initialize(cls):
        cls.default_headers = config.default_headers
        load_dotenv()
        return True

    @staticmethod
    def process_datetime(data, time_format='%H:%M:%S'):
        try:
            split_data = str(data).split('T')
            date = split_data[0]
            time = split_data[1].replace('Z', '')
            formatted_time = datetime.strptime(time, '%H:%M:%S').strftime(time_format)
            return date, formatted_time
        except (IndexError, ValueError):
            return '-', '-'

    @staticmethod
    def todays_auctions():
        try:
            auction_response = requests.get(config.source_url, headers=MainScraper.default_headers)
            response_data = auction_response.json()
            main_data = response_data['data']['saleList']['laterSales']

            for item in main_data:
                sale_name = item.get('saleName', '-')
                date, time = MainScraper.process_datetime(
                    item.get("auctionDateTimeInUTC", '-'))

                data_dict = {
                    'SaleName': sale_name,
                    'AuctionDate': date,
                    'AuctionTime': time
                }

                MainScraper.data_list.append(data_dict)
        
        except Exception as e:
            MainScraper.logger.error(f"Error fetching auction data: {e}")
    
    @staticmethod
    def create_json():
        try:
            timestamp = datetime.now().strftime("%Y%m%d%H%M%S") 
            json_file_name = f'.\Data\jsons\{timestamp}.json'
            with open(json_file_name, 'w') as json_file:
                json.dump(MainScraper.data_list, json_file, indent=2)
            MainScraper.logger.info(f"JSON file created successfully: {json_file_name}")

        except Exception as e:
            MainScraper.logger.error(f"Error creating JSON file: {e}")

    @staticmethod
    def save_to_csv():
        try:
            df = pd.DataFrame(MainScraper.data_list)
            timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
            file_name = f'.\Data\csv\{timestamp}.csv'
            if os.path.exists(file_name):
                os.remove(file_name)

            df.to_csv(file_name, index=False)
            MainScraper.logger.info(f"CSV file created successfully: {file_name}")

        except Exception as e:
            MainScraper.logger.error(f"Error saving data to CSV: {e}")

    @staticmethod
    def save_to_db():
        try:
            connection_str = f'postgresql://{os.getenv("DB_USER")}:{os.getenv("DB_PASSWORD")}@{os.getenv("DB_HOST")}/{os.getenv("DB_DATABASE")}'
            db = create_engine(connection_str)

            with db.connect() as conn:
                with psycopg2.connect(
                    host=os.getenv("DB_HOST"),
                    database=os.getenv("DB_DATABASE"),
                    user=os.getenv("DB_USER"),
                    password=os.getenv("DB_PASSWORD"),
                    port='5432'
                ) as connection:
                    connection.autocommit = True
                    cursor = connection.cursor()
                    cursor.execute('DROP TABLE IF EXISTS action_table')
                    insert_query = '''CREATE TABLE action_table
                    (
                        SaleName character varying(100),
                        AuctionDate date,
                        AuctionTime character varying(100)
                    )  '''
                    cursor.execute(insert_query)

                    df = pd.DataFrame(MainScraper.data_list)
                    df.to_sql('action_table', conn,if_exists='replace', index=False)
                    select_query = '''SELECT * FROM action_table;'''
                    cursor.execute(select_query)
                    for row in cursor.fetchall():
                        print(row)

            MainScraper.logger.info("Data saved to the database successfully")

        except Exception as e:
            MainScraper.logger.error(f"Error saving data to the database: {e}")

    @staticmethod
    def process_data(save_to_json=True, save_to_db=False):
        try:
            MainScraper.todays_auctions()
            if save_to_json:
                MainScraper.save_to_csv()
                MainScraper.create_json()
            if save_to_db:
                MainScraper.save_to_db()
        except Exception as e:
            MainScraper.logger.error(f"Error processing data: {e}")


if __name__ == '__main__':
    MainScraper.initialize()
    MainScraper.process_data(save_to_json=True, save_to_db=False)
