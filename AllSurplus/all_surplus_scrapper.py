import requests
import json
import config
from logs import Logger  
import datetime
import pandas as pd

class SurplusScrapper:

    data_list = list()
    logger = Logger('SurplusScrapper').log_obj

    @staticmethod
    def make_request(url):
        try:
            response = requests.post(url, headers=config.headers, data=config.payload)
            response.raise_for_status()
            SurplusScrapper.logger.info(f"Successful requested status code: {response.status_code}")
            return response.json()
        except requests.exceptions.RequestException as e:
            SurplusScrapper.logger.error(f"Error making request to {url}: {e}")
            return None

    @staticmethod
    def scrape_asset_data(result):
        try:
            account_id = result.get('accountId', '')
            asset_id = result.get('assetId', '')

            asset_url = f'https://maestro.lqdt1.com/assets/{asset_id}/{account_id}/false'
            asset_response = SurplusScrapper.make_request(asset_url)

            data_dict = {
                'AccountId': account_id,
                'AssetId': asset_id,
                'AssetName': asset_response.get('assetShortDesc', '').strip() or '-',
                'AssetAuctionStart': asset_response.get('assetAuctionStartDate', '').split('T')[0].strip() or '-',
                'AssetAuctionEnd': asset_response.get('assetAuctionEndDate', '').split('T')[0].strip() or '-',
                'SellerName': asset_response.get('sellerContactName', '') or '-',
                'SellerEmail': asset_response.get('sellerContactEmail', '') or '-',
                'SellerPhone': asset_response.get('sellerContactPhone', '') or '-',
            }

            SurplusScrapper.data_list.append(data_dict)
            SurplusScrapper.logger.info(f"Successfully added data to the list. list len: {len(SurplusScrapper.data_list)}")
        except Exception as e:
            SurplusScrapper.logger.error(f"Error scraping data for asset {asset_id}: {e}")

    @staticmethod
    def main_script():
        response = SurplusScrapper.make_request(config.main_url)

        if response:
            for result in response.get('assetSearchResults', []):
                SurplusScrapper.scrape_asset_data(result)
            timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
            csv_file_name = f'.\Data\CSV\{timestamp}.csv'
            df = pd.DataFrame(SurplusScrapper.data_list)
            df.to_csv(csv_file_name)
            return True
        else:
            return False

    @staticmethod
    def create_json():
        try:
            timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
            json_file_name = f'.\Data\Jsons\{timestamp}.json'
            with open(json_file_name, 'w') as json_file:
                json.dump(SurplusScrapper.data_list, json_file, indent=2)
            SurplusScrapper.logger.info(f"JSON file created successfully: {json_file_name}")
        except Exception as e:
            SurplusScrapper.logger.error(f"Error creating JSON file: {e}")

if __name__ == '__main__':
    if SurplusScrapper.main_script():
        SurplusScrapper.create_json()
