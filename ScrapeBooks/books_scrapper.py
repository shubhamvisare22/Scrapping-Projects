from bs4 import BeautifulSoup
import requests
import pandas as pd
import random
from logs import Logger
import json
import config
from datetime import datetime

class BookScraper:
    data_list = list()
    logger = Logger('BookScraper').log_obj

    @classmethod
    def make_request(cls, url):
        try:
            agent = random.choice(config.user_agents)
            response = requests.get(url, headers={'User-agent': agent})
            response.raise_for_status()
            return response
        except requests.exceptions.RequestException as e:
            cls.logger.error(f"Error making request to {url}: {e}")
            return None

    @classmethod
    def scrape_book_data(cls, link):
        try:
            agent = random.choice(config.user_agents)
            response = cls.make_request(link)
            if response:
                soup = BeautifulSoup(response.content, 'html.parser')

                name = soup.find('h1').text.strip()
                price = soup.find('p', class_='price_color').get_text().strip().replace('Â', '').replace("£","")
                desc = soup.find(lambda tag: tag.name == 'p' and not tag.attrs).text

                info_table = soup.find('table', attrs={'class': 'table table-striped'})
                info_table_data = info_table.find_all('td')

                upc = info_table_data[0].text
                product_type = info_table_data[1].text
                price_ex_tax = info_table_data[2].text.replace("£", "")
                price_inc_tax = info_table_data[3].text.replace("£", "")
                tax = info_table_data[4].text.replace("£", "")
                availability = info_table_data[5].text
                total_reviews = info_table_data[6].text

                rating = soup.find('p', class_='star-rating')
                attrs = rating['class'][1] if rating else '-'

                if attrs == 'One':
                    attrs = 1
                elif attrs == 'Two':
                    attrs = 2
                elif attrs == 'Three':
                    attrs = 3
                elif attrs == 'Four':
                    attrs = 4
                elif attrs == 'Five':
                    attrs = 5
                else:
                    attrs = '-'

                data_dict = {
                    'Book Name': name,
                    'Book Price': price,
                    'Ratings': attrs,
                    'Description': desc,
                    'UPC': upc,
                    'Product Type': product_type,
                    'Price Excluding Taxes': price_ex_tax,
                    'Price Including Taxes': price_inc_tax,
                    'Total Taxes': tax,
                    'Stocks Availability': availability,
                    'Total Reviews': total_reviews
                }

                cls.data_list.append(data_dict)
        except Exception as e:
            cls.logger.error(f"Error scraping book data from {link}: {e}")

    @classmethod
    def create_json(cls):
        try:
            timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
            json_file_name = f'.\Data\Jsons\output_data_{timestamp}.json'
            
            with open(json_file_name, 'w') as json_file:
                json.dump(cls.data_list, json_file, indent=2)
            cls.logger.info(f"JSON file created successfully: {json_file_name}")
        except Exception as e:
            cls.logger.error(f"Error creating JSON file: {e}")

    @classmethod
    def process_data(cls):
        pages = list(range(1, 4))
        for i in pages:
            url = f'http://books.toscrape.com/catalogue/category/books/fantasy_19/page-{i}.html'
            response = cls.make_request(url)

            if response:
                soup = BeautifulSoup(response.content, 'html.parser')
                all_info = soup.find_all('article', class_='product_pod')
                all_links = []

                for i in all_info:
                    init_link = "http://books.toscrape.com/catalogue/"
                    bk_link = i.find('h3').a.get('href').replace('../../../', '')
                    final_link = init_link + bk_link
                    all_links.append(final_link)

                for link in all_links:
                    cls.scrape_book_data(link)

        df = pd.DataFrame(cls.data_list)
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        
        df.to_csv(f'.\Data\CSV\{timestamp}.csv', index=False)
        cls.create_json()
        cls.logger.info("Data processing completed successfully.")

if __name__ == '__main__':
    BookScraper.process_data()
