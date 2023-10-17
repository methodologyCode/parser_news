import csv
import logging
from logging import Formatter

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler('debug.log', mode='a')
logger.addHandler(handler)
formatter = Formatter(
    '{asctime}, {levelname}, {message}', style='{'
)
handler.setFormatter(formatter)


def write_csv(data):
    with open('news.csv', 'a', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow((data['name'],
                         data['url']))


class FailedRequestApi(Exception):
    """Исключение для неудачного запроса."""
    pass
