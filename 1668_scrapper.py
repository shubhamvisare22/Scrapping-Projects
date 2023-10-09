import requests
import pandas as pd
from .constants import _1668_headers, _1668_cookies, _1668_data


def get_data():
    url = 'https://widget.1688.com/front/ajax/get_json_component.json'

    response = requests.post(url, cookies=cookies, headers=headers, data=data)
    response.raise_for_status()

    json_data = response.json()
    main_data = json_data['content']['result'][0]['data']['list']

    return main_data


def process_data(main_data):
    product_urls = [data['detailUrl'] for data in main_data]
    video_urls = [data['videoUrl'] for data in main_data]
    product_names = [data['title'] for data in main_data]
    old_prices = [data['oldPrice'] for data in main_data]
    current_prices = [data['currentPrice'] for data in main_data]

    df = pd.DataFrame({
        'product_url': product_urls,
        'video_url': video_urls,
        'product_name': product_names,
        'current_price': current_prices,
        'old_price': old_prices
    })

    return df


def save_to_csv(df, filename='alibaba.csv'):
    df.to_csv(filename, index=False)
    print(f"Data saved to {filename}.")


if __name__ == '__main__':

    cookies = _1668_cookies

    headers = _1668_headers

    data = _1668_data

    main_data = get_data()
    df = process_data(main_data)
    save_to_csv(df)
    print("Done.")
