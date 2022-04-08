import requests
import os
from dotenv import load_dotenv

base_url = "https://api.getgeoapi.com/v2/currency/"


def get_supported_currency(api_key):
    url = base_url + "list"
    params = {
        "api_key": api_key,
        "format": "json"
    }
    response = requests.get(url, params=params)
    return response.json()


def check_currency_supportivity(api_key, currency_code):
    data = get_supported_currency(api_key)
    return True if currency_code in data['currencies'] else False


def currency_conversion(api_key, base_currency, currency_to_convert_to, amount=1, format="json"):
    if check_currency_supportivity(api_key, base_currency) and check_currency_supportivity(api_key, currency_to_convert_to):
        url = base_url + "convert"
        params = {
            "api_key": api_key,
            "from": base_currency,
            "to": currency_to_convert_to,
            "amount": amount,
            "format": format
        }
        response = requests.get(url, params=params)
        return response.json()
    else:
        return {"message": "One of the currency code you entered is not supported or invalid."}


load_dotenv()
api_key = os.getenv("CURRENCY_API_KEY")

# data = check_currency_supportivity(api_key, "asdbhjavds")

data = currency_conversion(api_key, "NZD", "JPY")

print(data)
