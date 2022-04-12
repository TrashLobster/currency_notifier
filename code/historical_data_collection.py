import sqlite3
from datetime import date, datetime, timedelta
from dotenv import load_dotenv
from os import getenv
from currency_converter import CurrencyConverter

base_currency = "NZD"
currency_convert_to = "JPY"
load_dotenv()
api_key = getenv("CURRENCY_API_KEY")

converter = CurrencyConverter(api_key, base_currency, currency_convert_to)

def generate_db():
    connection = sqlite3.connect('exchange_rate.db')
    cur = connection.cursor()

    # if the date is already recorded in the database, then don't rewrite it again - runs once a day at 12 pm and record that amount
    # TODO: time it so this code below runs, once every day at a specific time
    try:
        for i in range(100, 170):
            date_checked = date.isoformat(datetime.today() - timedelta(days=i))
            date_in_datebase = cur.execute('SELECT EXISTS (SELECT date FROM exchange_rate WHERE date=:date)', {"date": date_checked}).fetchone()[0]
            match date_in_datebase:
                case 0:  # where the date is not found in record
                    response = converter.currency_conversion_historic(date=date_checked)
                    params = (response["updated_date"], converter.base_currency, converter.currency_to_convert_to, response["rates"][converter.currency_to_convert_to]["rate"])
                    cur.execute(f"INSERT INTO exchange_rate VALUES (?, ?, ?, ?)", params)
                    connection.commit()
                case 1:
                    pass
        print("Data saved to exchange_rate.db")
    except TypeError:
        print("Error - ran out of API calls today")

    cur.close()

if __name__ == "__main__":
    generate_db()
else:
    print("Only execute when run directly.")
