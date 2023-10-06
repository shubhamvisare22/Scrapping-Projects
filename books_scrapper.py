from bs4 import BeautifulSoup
import requests
import pandas as pd
import random
from constants import user_agents


# data holders
def scrapper():
    names = []
    prices = []
    ratings = []
    description = []
    Upc = []
    Product_type = []
    Price_ex_tax = []
    Price_inc_tax = []
    Tax = []
    Availability = []
    Total_reviews = []

    pages = list(range(1, 4))
    for i in pages:
        url = f'http://books.toscrape.com/catalogue/category/books/fantasy_19/page-{i}.html'

        agent = random.choice(user_agents)
        resp = requests.get(url, headers={'User-agent': agent})

        soup = BeautifulSoup(resp.content, 'html.parser')

        all_info = soup.find_all('article', class_='product_pod')
        all_links = []

        for i in all_info:
            init_link = "http://books.toscrape.com/catalogue/"
            bk_link = i.find('h3').a.get('href').replace('../../../', '')
            final_link = init_link + bk_link
            all_links.append(final_link)

        for link in all_links:
            r2 = requests.get(link, headers=agent).content
            bk_soup = BeautifulSoup(r2, 'html.parser')

            name = bk_soup.find('h1').text.strip()
            names.append(name)

            price = bk_soup.find(
                'p', class_='price_color').get_text().strip().replace('Â', '')
            prices.append(price)

            desc = bk_soup.find(lambda tag: tag.name ==
                                'p' and not tag.attrs).text
            description.append(desc)

            info_table = bk_soup.find(
                'table', attrs={'class': 'table table-striped'})
            info_table_data = info_table.find_all('td')

            upc = info_table_data[0].text
            Upc.append(upc)

            product_type = info_table_data[1].text
            Product_type.append(product_type)

            price_ex_tax = info_table_data[2].text
            Price_ex_tax.append(price_ex_tax)

            price_inc_tax = info_table_data[3].text
            Price_inc_tax.append(price_inc_tax)

            tax = info_table_data[4].text
            Tax.append(tax)

            availability = info_table_data[5].text
            Availability.append(availability)

            total_reviews = info_table_data[6].text
            Total_reviews.append(total_reviews)

            rating = bk_soup.find('p', class_='star-rating')
            attrs = rating['class'][1]

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
            ratings.append(attrs)

    df = pd.DataFrame({'Book Name': names, 'Book Price': prices, 'Ratings': ratings, 'Discreption': description, 'UPC': Upc, 'Product Type': Product_type,
                       'Price Excluding Taxes': Price_ex_tax, 'Price Including Taxes': Price_inc_tax, 'Total Taxes': Tax, 'Stocks Availability': Availability, 'Tatal Reviews': Total_reviews})

    df.to_csv('Data.csv', index=False)


scrapper()
