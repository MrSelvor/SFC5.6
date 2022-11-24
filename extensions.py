import json
import requests
from config import keys


class APIException(Exception):
    pass

class CryptoConverter:
    @staticmethod
    def get_price(quote: str,base:str,amount:str):

        if quote == base:
            raise APIException(f'Нельзя конвертировать одинаковые валюты.')

        try:
            quote_ticker = keys[quote]
        except KeyError:
            raise APIException(f'Валюта "{quote}" отсутствует в списке. Обратитесь к /values .')

        try:
            base_ticker = keys[base]
        except KeyError:
            raise APIException(f'Валюта "{base}" отсутствует в списке. Обратитесь к /values .')
        try:
            amount = float(amount)
        except ValueError:
            raise APIException(f'Введите число вместо "{amount}". Дробные числа записываются через точку.')

        url = (f"https://api.apilayer.com/currency_data/convert?to={base_ticker}&from={quote_ticker}&amount={amount}")

        payload = {}
        headers = {
            "apikey": "6C8sfheCdzoSkO2Z1vrxuDa2InXKJTrt"
        }

        response = requests.request("GET", url, headers=headers, data=payload)

        status_code = response.status_code

        total_base = json.loads(response.content)
        return total_base['result']