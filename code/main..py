import sqlite3
from datetime import date, datetime
from dotenv import load_dotenv
from os import getenv
from currency_converter import CurrencyConverter
import smtplib

base_currency = "NZD"
currency_convert_to = "JPY"

'''
we need to run the data today and save it to the database, and then exhaust the API to save as much dates to the database. 
If the date is saved to the database, then we don't need to run those dates again
'''
load_dotenv()
api_key = getenv("CURRENCY_API_KEY")
converter = CurrencyConverter(api_key, base_currency, currency_convert_to)
connection = sqlite3.connect('exchange_rate.db')
cur = connection.cursor()

# get data from today
today = date.isoformat(datetime.today())
date_in_datebase = cur.execute('SELECT EXISTS (SELECT date FROM exchange_rate WHERE date=:date)', {
                               "date": today}).fetchone()[0]
match date_in_datebase:
    case 0:  # where the date is not found in record
        response = converter.currency_conversion()
        params = (response["updated_date"], converter.base_currency, converter.currency_to_convert_to,
                  response["rates"][converter.currency_to_convert_to]["rate"])
        cur.execute(f"INSERT INTO exchange_rate VALUES (?, ?, ?, ?)", params)
        connection.commit()
    case 1:
        print("Today's data has already been added")

# fetchone() returns tuples
mean = cur.execute('SELECT AVG(rate) FROM exchange_rate').fetchone()[0]
upper = cur.execute(
    'SELECT date, rate FROM exchange_rate ORDER BY rate DESC LIMIT 1').fetchone()
top_ten = cur.execute('SELECT date, rate FROM exchange_rate WHERE date != :today ORDER BY rate DESC LIMIT 10', {
    'today': today}).fetchall()
tenth_rate = top_ten[9]
total_days = cur.execute('SELECT COUNT(date) FROM exchange_rate').fetchone()[0]
lower = cur.execute(
    'SELECT date, rate FROM exchange_rate ORDER BY rate ASC LIMIT 1').fetchone()
upper_mean = cur.execute('SELECT AVG(rate) FROM exchange_rate WHERE rate > :mean', {
                         'mean': mean}).fetchone()[0]
today_data = cur.execute('SELECT date, rate FROM exchange_rate WHERE date = :today', {
                         'today': today}).fetchone()

connection.close()

# rule: if the exchange rate of the day is higher than the upper_mean, and higher than the top five values from historics, then send email

email_sender = getenv("EMAIL_FROM")
email_sender_password = getenv("EMAIL_FROM_PASSWORD")
email_recipient = getenv("EMAIL_TO")

today_rate = today_data[1]
top_ten_message = ""
for date, rate in top_ten:
    top_ten_message += f"\t{date} : {rate}\n"
historic_breakdown_message = f"The mean for the past {total_days} days is: {mean} and the upper mean is {upper_mean}.\n\nThe highest rate is {upper[1]} on {upper[0]} and the lowest is {lower[1]} on {lower[0]}."

if today_rate > mean and today_rate > tenth_rate[1]:
    # note that gmail will be removing the insecured third party login option on 30 May 2022
    with smtplib.SMTP("smtp.gmail.com", port=587) as connection:
        connection.starttls()
        connection.login(user=email_sender, password=email_sender_password)
        connection.sendmail(
            from_addr=email_sender,
            to_addrs=email_recipient,
            msg=f"Subject:Today's exchange rate from {converter.base_currency} to {converter.currency_to_convert_to} is something to look into!"
                f"\n\nExchange rate from {converter.base_currency} to {converter.currency_to_convert_to} "
                f"is at {today_rate}!\n\nThe top ten historic rates from the past {total_days} days (not including today) are: \n\n" +
                top_ten_message + "\n" + historic_breakdown_message
        )
    print("Email sent. Let's exchange some money!")
else:
    print("Email not sent - the rate is no good!")
