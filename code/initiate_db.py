import sqlite3

connection = sqlite3.connect('exchange_rate.db')
cur = connection.cursor()

cur.execute('''CREATE TABLE exchange_rate
               (date text, currency_from text, currency_to text, rate real)''')

connection.commit()

connection.close()
