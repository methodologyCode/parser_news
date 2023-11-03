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


def get_news(soup, news, div_tag=None, a_tag=None, div_class=None,
             a_class=None, ria=None, rbc=None, tag=None):
    item_list = soup.find_all(div_tag or a_tag, class_=ria or rbc)

    for item in item_list:
        name = item.find(tag, class_=div_class or a_class).text
        url = item.find('a').get('href') if div_tag else item.get('href')

        data = {'name': name,
                'url': url
                }

        write_csv(data)
    return f'Новости {news} собраны'


def get_news_ria(soup):
    return get_news(soup, 'RIA', div_tag='div',
                    div_class='cell-list__item m-no-image',
                    ria='cell-list__list', tag='div')


def get_news_rbc(soup):
    return get_news(soup, 'RBC', a_tag='a', a_class='main__feed__title',
                    rbc='main__feed__link', tag='span')


def main():
    sites = {
        'RBC': get_news_rbc(get_html('https://rbc.ru')),
        'RIA': get_news_ria(get_html('https://ria.ru')),
    }
    for url in sites.keys():
        print(sites[url])


if __name__ == '__main__':
    main()
