import requests
from bs4 import BeautifulSoup
import pandas as pd
import json
from logs import Logger
from datetime import datetime
import config

class CosentinoScraper:
    logger = Logger('CosentinoScraper').log_obj

    def __init__(self, url):
        self.url = url
        self.data_list = list()
        

    def make_request(self, url):
        try:
            response = requests.get(url)
            response.raise_for_status()
            return response
        except requests.exceptions.RequestException as e:
            self.logger.error(f"Error making request to {url}: {e}")
            return None
        

    def scrape_data(self, maindiv):
            try:
                for i in maindiv:
                    link = i.find('a').get('href') or '-'
                    title = i.find('div', class_='title').text.strip() or '-'
                    subtitle = i.find('div', class_='subtitle').text.strip() or '-'

                    link_resp = self.make_request(link)
                    if link_resp:
                        link_soup = BeautifulSoup(link_resp.content, 'html.parser')

                        thik_div = link_soup.find('div', class_='espesores block_content')
                        thickness = thik_div.text.strip().replace('\n\n\n\n\n\n', '  ').replace(',', '.').replace('  ', ',') if thik_div else '-'

                        format_div = link_soup.find('div', class_='formatos block_content')
                        formats = ' '.join(format_div.text.strip().split()) if format_div else '-'

                        data_dict = {
                            'Title': title,
                            'Subtitle': subtitle,
                            'Thickness': thickness,
                            'Format': formats,
                            'Product Link': link
                        }

                        self.data_list.append(data_dict)
            except Exception as e:
                self.logger.error(f"Error scraping data: {e}")
                

    def create_json(self):
        try:
            timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
            json_file_name = f'.\Data\Jsons\{timestamp}.json'
            with open(json_file_name, 'w') as json_file:
                json.dump(self.data_list, json_file, indent=2)
            self.logger.info(f"JSON file created successfully: {json_file_name}")
        except Exception as e:
            self.logger.error(f"Error creating JSON file: {e}")
            
            
    def process_data(self):
        try:
            response = self.make_request(self.url)
            if response:
                soup = BeautifulSoup(response.content, 'html.parser')
                maindiv = soup.find_all('div', class_='col-6 col-md-4 col-lg-3 inspiration')

                self.scrape_data(maindiv)

                df = pd.DataFrame(self.data_list)
                timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
                df.to_csv(f'.\Data\CSV\{timestamp}.csv', index=False)
                self.create_json()
                self.logger.info("Data processing completed successfully.")
        except Exception as e:
            self.logger.error(f"Error processing data: {e}")



if __name__ == '__main__':    
    scraper = CosentinoScraper(config.url)
    scraper.process_data()
