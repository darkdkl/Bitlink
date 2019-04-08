import requests
import os
import argparse

from urllib.parse import urlparse
from dotenv import load_dotenv
load_dotenv()
TOKEN = os.getenv('TOKEN')


def make_shorter(url, key):
    key = 'Bearer {}'.format(key)
    headers = {'Authorization': key}
    json = {"long_url": url}
    url_for_shorten = "https://api-ssl.bitly.com/v4/shorten"
    short_link = requests.post(url_for_shorten, json=json, headers=headers)
    if short_link.ok:
        return short_link.json()['link']


def prepare_link(link):
    prepared_link = urlparse(link)
    return prepared_link.netloc+prepared_link.path


def return_clicks(short_url, key):

    url_for_click = 'https://api-ssl.bitly.com/v4/bitlinks/{}/clicks/summary'\
        .format(prepare_link(short_url))
    headers = {'Authorization': key}
    clicks_params = {'unit': 'day', 'units=': -1}
    clicks = requests.get(url_for_click, headers=headers, params=clicks_params)
    return clicks.json()


def check_link(link, key):
    url = 'https://api-ssl.bitly.com/v4/bitlinks/{}'.format(prepare_link(link))
    headers = {'Authorization': key}
    response = requests.get(url, headers=headers)
    return response.ok


def main(apikey):

    parser = argparse.ArgumentParser(
        description=' Программа для сокращения ссылок')
    parser.add_argument('url', help='Введите вашу ссылку')

    args = parser.parse_args()
    
    if check_link(args.url, apikey):
        print('')
        print('Количество переходов :', return_clicks(
            args.url, apikey)['total_clicks'])
        print('')

    elif make_shorter(args.url, apikey):
        print('*'*50)
        print('Ваша короткая ссылка :', make_shorter(args.url, apikey))
        print('*'*50)
    else:
        print('Введеное значение не является корректной ссылкой')


if __name__ == "__main__":
    main(TOKEN)
