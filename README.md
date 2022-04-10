# Currency Notifier

**DISCLAIMER:**

This project was designed solely for study and for personal use only.

**NOTE:** the automated email sending will no longer be usable after 30 May 2022 as Google will be removing the less secured login in option then

**Background/goal:**

This project came about from a trip long in the waitings. My friends and I want to go travelling in Japan in less than two years time and I thought that it would be a cool challenge to see if I could set up an alert to track what the exchange rate beteween NZD and JPY is. I plan on setting up a function to email me when a certain threshold is met. Due to limitation of the free tier subscription to the Currency API, I can only make a maximum of 100 calls a day, which is more than enough to refresh once a day.

**Dependencies:**

  - API - I am using the Currency API (see documentation here: https://currency.getgeoapi.com/documentation/) to gather current and historical exchange rates
  - sqlite3 - i am using a .db file to store the information to then obtain mean, median etc. 
  - dotenv - to store API-keys and email logins

**Sample email:**

Subject: Exchange rate from NZD to JPY is at 85.0587!

The top ten historic rates from the past 100 days (not including today) are:

    2022-04-06 : 86.0797
    2022-04-05 : 86.0701
    2022-03-28 : 85.8252
    2022-04-07 : 85.5589
    2022-04-04 : 85.1702
    2022-03-29 : 85.1252
    2022-04-01 : 85.0669
    2022-04-08 : 85.0587
    2022-04-02 : 84.9986
    2022-03-30 : 84.9501

The mean for the past 100 days is: 79.27097900000003 and the upper mean is 83.19558437499998.

The highest rate is 86.0797 on 2022-04-06 and the lowest is 75.5563 on 2022-01-28.
