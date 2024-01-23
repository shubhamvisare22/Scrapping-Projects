''' ------------------------------------- Requirements ----------------------------------------- '''
import requests
from bs4 import BeautifulSoup
import pandas as pd
import re
from retrying import retry
import datetime
from .config import default_headers as def_headers


class EnergyScrapper():

    def __init__(self):

        self.all_data = {
            'seller_company': [],
            'seller_name': [],
            'seller_phone': [],
            'seller_email': [],
            'seller_website': [],
            'seller_fax': [],
            'seller_address': [],
            'seller_url_list': []
        }

        self.default_headers = def_headers

    ''' --------------------------------- Helper Functions -------------------------- '''
    @retry(stop_max_attempt_number=3, wait_fixed=int(0.5 * 1000))
    def make_request(self, url):
        response = requests.get(url, headers=self.default_headers)
        try:
            if response.status_code != 200:
                raise ValueError(f"Request failed with status code {response.status_code}")
        except Exception as e:
            print(f"Retry Exception while scrapping --> {url} --> {e} \nStatus code --> {response.status_code}")
        return response

    # DATA CLEANING AND EXTRACTION
    def extract_seller_phone_numbers(self, text):
        phone_pattern = re.compile(r'(?:Phone: |Phone 2: |Phone:|Phone 2:|Phone : |Phone 2 :|Phone2 : |Phone2:|Phone 2: |Call：)\s*\s*([^:\n]+?)\s*(?=\b(?:Phone|Phone 2|Web|Email|Fax| &nbspWeb| &nbspEmail| &nbspPhone 2|&nbspFax| )\b|$)')
        phones = phone_pattern.findall(text)
        return list(set(phones)) if phones else '-'

    def extract_email(self, text):
        email_pattern = re.compile(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b')
        emails = [e.replace('https', '').replace('http', '').replace('%20', '').replace(' s', '').strip() for e in email_pattern.findall(text.replace('.com', '.com ').replace('Web:', ' ').lower())]
        return list(set(emails)) if emails else '-'

    def extract_fax(self, text):
        fax_pattern = re.findall(r"Fax: \((\d{3})\) (\d{3}-\d{4})", str(text))
        fax = '({}) {}'.format(
            fax_pattern[0][0], fax_pattern[0][1]) if fax_pattern else '-'
        return fax

    def extract_website(self, text):
        websites = re.findall(r"(?i)\b(?:http://|https?://|www\.)\S+\b(?<!\W)",text.replace('.com', '.com ').replace('Web:', ' '))
        unique_websites = list(set(re.sub(r"(?i)^(?:http://|https?://)?", "", website.lower()) for website in websites))
        return list(set(unique_websites)) if unique_websites else '-'

    def extract_name(self, text):
        if text:
            name_pattern = re.compile(r'(?: Contact:)\s*([^:\n]+)(?=\s+(?:Phone|Fax|Phone 2|Web|Email|&nbsp|  Call):|\n)')
            name_pattern2 = re.compile(r'Contact：(.*?)(?=\s*(?:Call|Phone|Fax|Phone 2|Web|Email|&nbsp|$))')
            matches = re.findall(name_pattern, text) or re.findall(
                name_pattern2, text)
            name = matches[0] if matches else '-'
            name = '-' if '@' in name else name
            return name
        return '-'

    def extract_product_phone(self, text):
        replacements = ['call', 'CALL', '-summary','Call：', 'FOR', 'PRICE', '%20']
        cleaned_text = re.sub('|'.join(replacements), '', text).strip()
        return self.data_validation(cleaned_text) if cleaned_text and (cleaned_text[0].isdigit() or cleaned_text[0] == '+' or cleaned_text[0] == '(') else '-'

    def data_validation(self, data):
        return data if data else '-'

    def extract_desc(self, text):
        desc_pattern = r'(?:Detailed Description|Detailed description)(.*)'
        matches = re.findall(desc_pattern, text, re.DOTALL)
        desc = str(matches[0]).replace('聽', ' ').replace(
            '戮', ' ').strip().capitalize() if matches else '-'
        return desc

    def clean_product_name(self, text):
        return str(text).replace('NOT SPECIFIED', '').replace('For Sale', ' ').strip().title()

    def process_product_address(self, p_tags, ul_tags, span_tags, product_name):
        break_keywords = ['Email', 'http', 'Call','call', 'Detailed', 'detailed', 'CALL']
        continue_keywords = ['Contact', 'Contect','contact', 'CONTACT', 'contect', f'{product_name}']
        product_address = ''
        producat_contact_name = ''
        for tag in p_tags:
            if tag.name == "p":
                text = tag.text
                if text:
                    if any(keyword in text for keyword in break_keywords):
                        break
                    if any(keyword in text for keyword in continue_keywords) or tag.find("strong") or tag.find("h3"):
                        if ':' in tag.text:
                            producat_contact_name = tag.text.split(':')[1]
                        continue
                    product_address += ' ' + text

        if not product_address:
            for tag in ul_tags:
                if tag.name == "ul":
                    text = tag.text
                    if text:
                        if any(keyword in text for keyword in break_keywords):
                            break
                        if any(keyword in text for keyword in continue_keywords) or tag.find("strong") or tag.find("h3"):
                            continue
                        product_address += ' ' + text

        if not product_address:
            for tag in span_tags:
                if tag.name == "span":
                    text = tag.text
                    if text:
                        if any(keyword in text for keyword in break_keywords):
                            if 'Callahan' not in text:
                                break
                        if any(keyword in text for keyword in continue_keywords) or tag.find("strong") or tag.find("h3"):
                            if ':' in tag.text:
                                producat_contact_name = tag.text.split(':')[1]
                            continue
                        product_address += ' ' + text

        if producat_contact_name in product_address:
            product_address = product_address.replace(producat_contact_name, '')
        if '( Direct ph. +47 5553 8487 )' in product_address:
            product_address = product_address.replace('( Direct ph. +47 5553 8487 )', '')
        return product_address.title().replace('\n', ' ').strip()

    def clean_product_name(self, text):
        return text.replace(',', ' ').replace('custom Title', '').replace('Custom title', '').strip().title() if text else ''

    def exctract_seller_info(self, seller_text):
        seller_name = self.extract_name(seller_text)
        seller_phone = self.extract_seller_phone_numbers(seller_text)
        seller_email = self.extract_email(seller_text)
        seller_website = self.extract_website(seller_text)
        seller_fax = self.extract_fax(seller_text)
        return seller_name, seller_phone, seller_email, seller_website, seller_fax

    ''' --------------------- Scraping starts here --------------------------------- '''

    def MainScript(self):
        counter = 7
        total_pages = 0

        while True:
            url = f'https://energyard.com/index.php?route=multiseller/home&seller_id={counter}'
            print(f'\nScraping User: --> {url}')
            counter += 1

            if counter == 10:
                break

            main_page_response = self.make_request(url)
            main_soup = BeautifulSoup(
                main_page_response.content, 'html.parser')
            main_page_divs = main_soup.find_all('div', {'class': re.compile(
                r'product-layout product-grid col-md-(3|4) col-sm-6')})

            if not main_page_divs:
                print('Empty Seller')
                continue

            for i in main_page_divs[:1]:

                seller_info_div1 = main_soup.find_all('div', 'col-xs-12')
                seller_info_div2 = main_soup.find_all('div', 'seller-modules-heading')

                try:

                    ''' Information here getting scrapped from seller pages'''

                    if seller_info_div1 is not None:
                        seller_text = ' '.join([div.get_text().strip().replace('&nbsp', ' ') for div in seller_info_div1])
                        seller_name, seller_phone, seller_email, seller_website, seller_fax = self.exctract_seller_info(seller_text)

                        if (seller_name == '-' or seller_phone == '-' or seller_email == '-' or seller_website == '-' or seller_fax == '-') and seller_info_div2 is not None:
                            seller_text = ' '.join([div.get_text().strip().replace('&nbsp', ' ') for div in seller_info_div2])
                            seller_name, seller_phone, seller_email, seller_website, seller_fax = self.exctract_seller_info(seller_text)
                            seller_name = seller_name.replace('&nbsp', '').strip().title() if seller_name else '-'

                        try:
                            product_url = i.find('a').get('href')
                            print(f'Scraping Product: --> {product_url}')
                            product_response = self.make_request(product_url)
                        except Exception as e:
                            print('Product Request Exception:', e)

                        product_soup = BeautifulSoup(product_response.content, 'html.parser')
                        product_div = product_soup.find('div', {'id': 'tab-description'})

                        ''' Information here getting scrapped from product pages,
                        finally compare the availabe information and store that to csv 
                        '''
                        if product_div is not None:

                            '''-------------------------Seller Email ------------------------- '''
                            product_email = product_div.text
                            if seller_email != self.extract_email(product_email):
                                seller_email = ', '.join(email for email in self.extract_email(product_email))

                            '''------------------------- Seller Website ------------------------- '''

                            product_website = '  '.join([div.text.replace('.com', '.com  ').replace('www', ' www').replace('Call', ' Call').strip() for div in product_div])
                            if seller_website != self.extract_website(product_website):
                                seller_website = ', '.join(website for website in self.extract_website(product_website))

                            ''' ------------------------- Seller Phone Number -------------------------'''

                            product_phone1 = product_soup.find('div', 'col-md-7 col-sm-6 product-description').find('h2', 'title-summary')
                            product_phone_number = self.extract_product_phone(product_phone1.text) if product_phone1 else ''

                            product_phone2 = product_soup.find('div', 'col-md-7 col-sm-6 product-description').find('div', 'product-price-wrapper').find('span', 'price-new')
                            if product_phone2 and not product_phone_number:
                                product_phone_number = self.extract_product_phone(product_phone2.text)

                            if seller_phone != product_phone_number:
                                seller_phone = product_phone_number

                            ''' ------------------------- Seller Company Name ------------------------- '''

                            final_name1 = main_soup.find('div', 'col-xs-12').h1 or main_soup.find('div', 'col-xs-12').h2
                            final_name1 = final_name1.text if final_name1 else ''

                            name1 = product_soup.find('div', 'col-md-7 col-sm-6 product-description').find(
                                'div', 'product-seller-info').find('p', 'avatar-name')
                            name2 = product_soup.find('div', {'id': 'tab-description'}).strong or product_soup.find('div', {'id': 'tab-description'}).h3
                            final_name = self.clean_product_name(name1.text) if name1 else ''

                            if name1 and name2 and name1.text.split(' ')[0:2] == name2.text.split(' ')[0:2]:
                                final_name = name2.text

                            product_company = final_name if len(final_name1) < len(final_name) else final_name1
                            seller_company = self.clean_product_name(product_company)

                            '''----------------------- Seller Address ------------------------- '''
                            p_tags, ul_tags, span_tags, product_avatar_name = product_div.find_all('p'), product_div.find_all('ul'), product_div.find_all('span'), product_soup.find('p', {'class': 'avatar-name'}).text
                            seller_address = self.process_product_address(p_tags, ul_tags, span_tags, product_avatar_name)

                            if seller_name in seller_address:
                                seller_address = seller_address.replace(seller_name, '').strip()

                            ''' ------------------- Data storing --------------------------'''
                            self.all_data['seller_name'].append(seller_name)
                            self.all_data['seller_phone'].append(seller_phone)
                            self.all_data['seller_email'].append(seller_email)
                            self.all_data['seller_website'].append(seller_website)
                            self.all_data['seller_fax'].append(seller_fax)
                            self.all_data['seller_company'].append(seller_company)
                            self.all_data['seller_address'].append(seller_address)

                    else:
                        self.all_data['seller_name'].append('-')
                        self.all_data['seller_phone'].append('-')
                        self.all_data['seller_email'].append('-')
                        self.all_data['seller_website'].append('-')
                        self.all_data['seller_fax'].append('-')
                        self.all_data['seller_company'].append('-')
                        self.all_data['seller_address'].append('-')

                    self.all_data['seller_url_list'].append(url)
                    total_pages += 1
                except Exception as e:
                    print('Seller Data Exception:', e)

            print("Last Seller Id visited:", (counter - 1))
            print("Total Webpages Scrapped:", total_pages)

    def run_scrapper(self):

        self.MainScript()

        try:
            print('......................Creating DataFrame.......................')
            df = pd.DataFrame(self.all_data)
            print('...................Creating CSV....................')
            unix_time = int(datetime.datetime.now(datetime.timezone.utc).timestamp())
            file_name = f'Data_{unix_time}.csv'
            df.to_csv(file_name, index=False)
            print(f'All Done... CSV created... {file_name}')
        except Exception as e:
            print('DataFrame Exception:', e)
        print('Done............')


if __name__ == '__main__':
    scrapper = EnergyScrapper()
    scrapper.run_scrapper()
