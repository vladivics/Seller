import requests
import json


# Ozon api info (must be in .ini file later)
CLIENT_ID = '30846'
API_KEY = 'b5d1c965-7725-4615-b3b7-2cbdd9899d3f'

# Ozon method info
OZON_API_URL = 'https://api-seller.ozon.ru'
OZON_API_METHOD = '/v3/posting/fbs/unfulfilled/list'


def parse_json_response(data):
    result = {
        'header': ['order_id', 'price', 'name', 'delivering_date'],
        'data': []
    }
    for index in range(len(data)):
        for product in data[index]['products']:
            result['data'].append([data[index]['order_id'], product['price'],
                                   product['name'], data[index]['delivering_date']])
    return result


def get_parsed_request(delivering_date_from, delivering_date_to, url=OZON_API_URL, method=OZON_API_METHOD):
    head = {
        'Client-Id': CLIENT_ID,
        'Api-Key': API_KEY
    }
    body = {
        'dir': 'ASC',
        'filter': {
            'delivering_date_from': delivering_date_from,
            'delivering_date_to': delivering_date_to,
        },
        'limit': 100
    }
    body = json.dumps(body)
    response = requests.post(url + method, headers=head, data=body).json()['result']['postings']
    return parse_json_response(response)
