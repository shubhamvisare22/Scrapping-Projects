import requests
from bs4 import BeautifulSoup
import pandas as pd


def scrapper(url):
    resp = requests.get(url)
    soup = BeautifulSoup(resp.content, 'html.parser')
    maindiv = soup.find_all('div', class_='col-6 col-md-4 col-lg-3 inspiration')

    links = []
    titles = []
    subtitles = []
    thikness = []
    formats = []

    for i in maindiv:
        link = i.find('a').get('href')
        links.append(link)

        title = i.find('div', class_='title')
        titles.append(title.text.strip())

        subtitle = i.find('div', class_='subtitle')
        subtitles.append(subtitle.text.strip())

    for i in links:
        link_resp = requests.get(i)
        link_soup = BeautifulSoup(link_resp.content, 'html.parser')

        thik_div = link_soup.find('div', class_='espesores block_content')
        if thik_div is not None:
            thikness.append(thik_div.text.strip().replace(
                '\n\n\n\n\n\n', '  ').replace(',', '.').replace('  ', ','))
        else:
            thik_div = '-'
            thikness.append(thik_div)

        format_div = link_soup.find('div', class_='formatos block_content')
        if format_div is not None:
            test = format_div.text.strip().join('  ').strip().split()
            listToStr = ' '.join(map(str, test))
            formats.append(listToStr)
        else:
            format_div = '-'
            formats.append(format_div)

    df = pd.DataFrame({'Title': titles, 'Subtitle': subtitles,
                       'Thickness': thikness, 'Format': formats, 'Product Link': links})
    df.to_csv('Contesino.csv')


url = 'https://www.cosentino.com/usa/colors/'
scrapper(url)
