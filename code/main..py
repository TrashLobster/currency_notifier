import sqlite3
from datetime import date, datetime, timedelta
from dotenv import load_dotenv
from os import getenv
from currency_functions import *

BASE_CURRENCY = "NZD"
CURRENCY_CONVERT_TO = "JPY"

# TODO: Currency API (using Currency API, see documentation - https://currency.getgeoapi.com/documentation/) - retrieve historic data for the past two years between NZD and JPY
'''
we need to run the data today and save it to the database, and then exhaust the API to save as much dates to the database. 
If the date is saved to the database, then we don't need to run those dates again
'''
load_dotenv()
api_key = getenv("CURRENCY_API_KEY")

connection = sqlite3.connect('exchange_rate.db')
cur = connection.cursor()

# if the date is already recorded in the database, then don't rewrite it again - runs once a day at 12 pm and record that amount
# TODO: time it so this code below runs, once every day at a specific time
for i in range(0, 10):
    date_checked = date.isoformat(datetime.today() - timedelta(days=i))
    print(date_checked)
    date_in_datebase = cur.execute('SELECT EXISTS (SELECT date FROM exchange_rate WHERE date=:date)', {"date": date_checked}).fetchone()[0]
    match date_in_datebase:
        case 0:  # where the date is not found in record
            response = currency_conversion_historic(api_key, BASE_CURRENCY, CURRENCY_CONVERT_TO, date=date_checked)
            print(response)
            params = (response["updated_date"], BASE_CURRENCY, CURRENCY_CONVERT_TO, response["rates"][CURRENCY_CONVERT_TO]["rate"])
            print(params)
            cur.execute(f"INSERT INTO exchange_rate VALUES (?, ?, ?, ?)", params)
            connection.commit()
        case 1:
            pass

# print(cur.execute('SELECT * FROM exchange_rate').fetchall())

# TODO: Data analysis, find max, min, mean, upper quartile, lower quartile
# TODO: connect to email - if the exchange rate is higher than upper quartile, send an email to main email

connection.close()