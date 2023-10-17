from http import HTTPStatus

import requests
from bs4 import BeautifulSoup

from utils import logger, FailedRequestApi, write_csv


def get_html(url):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'
                             'AppleWebKit/537.36 (KHTML, like Gecko)'
                             'Chrome/102.0.0.0 Safari/537.36'}

    try:
        response = requests.get(url, headers=headers)
    except requests.exceptions.RequestException as e:
        logger.critical(f'Запрос провалился: {e}')
        raise FailedRequestApi(f'Запрос провалился: {e}')

    if response.status_code != HTTPStatus.OK:
        logger.error(f'Ответ сервера: {response.status_code}')
        raise FailedRequestApi(f'Ответ сервера: {response.status_code}')

    return BeautifulSoup(response.text, 'lxml')


def get_news_ria(soup):
    div_list = soup.find_all('div', class_='cell-list__list')

    for item in div_list:
        name = item.find('div',
                         class_='cell-list__item m-no-image').text[0:-5]
        url = item.find('a').get('href')

        data = {'name': name,
                'url': url
                }

        write_csv(data)
    return "RIA новости собраны"


def get_news_rbc(soup):
    a_list = soup.find_all('a', class_='main__feed__link')

    for item in a_list:
        name = item.find('span', class_='main__feed__title').text
        url = item.get('href')

        data = {'name': name,
                'url': url
                }

        write_csv(data)
    return "RBC новости собраны"


def get_news():
    sites = {
        'RBC': get_news_rbc(get_html('https://rbc.ru')),
        'RIA': get_news_ria(get_html('https://ria.ru')),
    }
    for url in sites.keys():
        print(sites[url])


if __name__ == '__main__':
    get_news()
