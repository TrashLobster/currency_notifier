import requests

base_url = "https://api.getgeoapi.com/v2/currency/"


class CurrencyConverter:
    def __init__(self, api_key, base_currency, currency_to_convert_to):
        self.api_key = api_key
        self.base_currency = base_currency
        self.currency_to_convert_to = currency_to_convert_to

    def get_supported_currency(self):
        url = base_url + "list"
        params = {
            "api_key": self.api_key,
            "format": "json"
        }
        response = requests.get(url, params=params)
        return response.json()

    def check_currency_supportivity(self):
        data = self.get_supported_currency()
        return True if self.currency_code in data['currencies'] else False

    def currency_conversion(self, amount=1, format="json"):
        url = base_url + "convert"
        params = {
            "api_key": self.api_key,
            "from": self.base_currency,
            "to": self.currency_to_convert_to,
            "amount": amount,
            "format": format
        }
        response = requests.get(url, params=params)
        if response.json()['status'] == "failed" or response.json()['status'] == "fail":
            return f"ERROR: {response.json()['error']['message']}"
        return response.json()

    def currency_conversion_historic(self, date, amount=1, format='json'):
        # date must be entered in a YYYY-MM-DD format
        url = f"{base_url}historical/{date}"
        params = {
            "api_key": self.api_key,
            "from": self.base_currency,
            "to": self.currency_to_convert_to,
            "amount": amount,
            "format": format
        }
        response = requests.get(url, params=params)
        if response.json()['status'] == "failed" or response.json()['status'] == "fail":
            return f"ERROR: {response.json()['error']['message']}"
        return response.json()
