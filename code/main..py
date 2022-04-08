import sqlite3
from datetime import date, datetime, timedelta
from dotenv import load_dotenv
from os import getenv
from currency_functions import *

BASE_CURRENCY = "NZD"
CURRENCY_CONVERT_TO = "JPY"

'''
we need to run the data today and save it to the database, and then exhaust the API to save as much dates to the database. 
If the date is saved to the database, then we don't need to run those dates again
'''
load_dotenv()
api_key = getenv("CURRENCY_API_KEY")

connection = sqlite3.connect('exchange_rate.db')
cur = connection.cursor()

# get data from today
date_in_datebase = cur.execute('SELECT EXISTS (SELECT date FROM exchange_rate WHERE date=:date)', {"date": date.isoformat(datetime.today())}).fetchone()[0]
match date_in_datebase:
    case 0:  # where the date is not found in record
        response = currency_conversion(api_key, BASE_CURRENCY, CURRENCY_CONVERT_TO)
        params = (response["updated_date"], BASE_CURRENCY, CURRENCY_CONVERT_TO, response["rates"][CURRENCY_CONVERT_TO]["rate"])
        cur.execute(f"INSERT INTO exchange_rate VALUES (?, ?, ?, ?)", params)
        connection.commit()
    case 1:
        print("Today's data has already been added")

mean = cur.execute('SELECT AVG(rate) FROM exchange_rate').fetchone()[0]
upper = cur.execute('SELECT rate FROM exchange_rate ORDER BY rate DESC LIMIT 1').fetchone()[0]
lower = cur.execute('SELECT rate FROM exchange_rate ORDER BY rate ASC LIMIT 1').fetchone()[0]
print(mean, upper, lower)

for row in cur.execute('SELECT * FROM exchange_rate ORDER BY date'):
    print(row)
# TODO: Data analysis, find max, min, mean, upper quartile, lower quartile
# TODO: connect to email - if the exchange rate is higher than upper quartile, send an email to main email

connection.close()