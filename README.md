# currency_notifier

Background/goal:
This project came about from a trip long in the waitings. My friends and I want to go travelling in Japan in less than two years time and I thought that it would be a cool challenge to see if I could set up an alert to track what the exchange rate beteween NZD and JPY is. I plan on setting up a function to email me when a certain threshold is met. Due to limitation of the free tier subscription to the Currency API, I can only make a maximum of 100 calls a day, which is more than enough to refresh once a day.

Dependencies:
  - API - I am using the Currency API (see documentation here: https://currency.getgeoapi.com/documentation/) to gather current and historical exchange rates
  - sqlite3 - i am using a .db file to store the information to then obtain mean, median etc. 
  - dotenv - to store API-keys and email logins
  - Haraka (?) - email server
