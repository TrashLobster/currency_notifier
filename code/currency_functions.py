import requests
import os
from dotenv import load_dotenv
from datetime import date, datetime, timedelta

# TODO: Currency API (using Currency API, see documentation - https://currency.getgeoapi.com/documentation/) - retrieve historic data for the past two years between NZD and JPY
# TODO: Data analysis, find max, min, mean, upper quartile, lower quartile
# TODO: connect to email - if the exchange rate is higher than upper quartile, send an email to main email

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
    url = base_url + "convert"
    params = {
        "api_key": api_key,
        "from": base_currency,
        "to": currency_to_convert_to,
        "amount": amount,
        "format": format
    }
    response = requests.get(url, params=params)
    if response.json()['status'] == "failed" or response.json()['status'] == "fail":
        return f"ERROR: {response.json()['error']['message']}"
    return response.json()


# date must be entered in a YYYY-MM-DD format
def currency_conversion_historic(api_key, base_currency, currency_to_convert_to, date, amount=1, format='json'):
    url = f"{base_url}historical/{date}"
    params = {
        "api_key": api_key,
        "from": base_currency,
        "to": currency_to_convert_to,
        "amount": amount,
        "format": format
    }
    response = requests.get(url, params=params)
    if response.json()['status'] == "failed" or response.json()['status'] == "fail":
        return f"ERROR: {response.json()['error']['message']}"
    return response.json()

load_dotenv()
api_key = os.getenv("CURRENCY_API_KEY")

# data = check_currency_supportivity(api_key, "asdbhjavds")

# data = currency_conversion(api_key, "NZD", "JPY")

# data = historical_currency(api_key, "NZD", "JPY", "2021-03-28")

# print(data)

