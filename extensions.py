import requests
import json
from TOKEN import keys

class APIException(Exception):
    pass

class CurrencyExchangeConvertion:
    @staticmethod
    def get_price(base: str, quote: str, amount: str):
        if base == quote:
            raise APIException('Валюты совпадают')

        try:
            base_ticker = keys[base]
        except KeyError:
            raise APIException(f'Неверно введена валюта {base}.\nВоспользуйтесь командой /values , чтобы увидеть, как правильно вводится наименование валюты.')

        try:
            quote_ticker = keys[quote]
        except KeyError:
            raise APIException(f'Неверно введена валюта {quote}.\nВоспользуйтесь командой /values , чтобы увидеть, как правильно вводится наименование валюты.')

        try:
            amount = float(amount)
        except ValueError:
            raise APIException('Неверно введено количество валюты. Количество вводится в цифровом формате.')

        r = requests.get(f'https://api.fastforex.io/convert?from={base_ticker}&to={quote_ticker}&amount={amount}&api_key=f2509762ad-3fc6df1fe2-r01tjj')
        result = json.loads(r.content)['result']
        total_base = result[keys[quote]]
        return total_base
