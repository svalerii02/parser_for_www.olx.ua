import requests
from bs4 import BeautifulSoup
import csv
import os

HOST = 'https://www.olx.ua'
URL = 'https://www.olx.ua/transport/moto/mototsikly/'
HEADERS = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)' 
                         'Chrome/85.0.4183.121 Safari/537.36 OPR/71.0.3770.287',
           'accept': '*/*'
           }
FILE = 'moto.csv'


def get_html(url, params=None):
    r = requests.get(url, headers=HEADERS, params=params)
    return r


def get_pages_count(html):
    soup = BeautifulSoup(html, 'html.parser')
    pagination = soup.find_all('span', class_='item fleft')
    if pagination:
        return int(pagination[-1].get_text())
    else:
        return 1
    print(pagination)


def get_content(html):
    soup = BeautifulSoup(html, 'html.parser')
    items = soup.find_all('tr', class_='wrap')
    moto = []
    for item in items:
        moto.append({'title': item.find('h3', class_='lheight22 margintop5').get_text(strip=True),
                     'link': item.find('a').get('href')
                     })
    return moto


def save_file(items, path):
    with open(path, 'w', encoding='utf-8', newline='') as file:
        writer = csv.writer(file, delimiter=',')
        writer.writerow(['Название', 'Ссылка'])
        for item in items:
            writer.writerow([item['title'], item['link']])


def parse():
    html = get_html(URL)
    if html.status_code == 200:
        moto = []
        pages_count = get_pages_count(html.text)
        for page in range(1, pages_count + 1):
            print(f'Парсинг страницы {page} из {pages_count}...')
            html = get_html(URL, params={'page': page})
            moto.extend(get_content(html.text))
        save_file(moto, FILE)
        print(f'Получено {len(moto)} вариантов.')
        print(moto)
        os.startfile(FILE)
    else:
        print('Error')


parse()
