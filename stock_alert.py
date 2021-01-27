#   stock_alert.py
# Sends 3 SMS msgs with articles about the stock being followed explaining apparent increase or decrease

import requests
from twilio.rest import Client
import secret

STOCK_NAME = "TSLA"
COMPANY_NAME = "Tesla Inc"

STOCK_ENDPOINT = "https://www.alphavantage.co/query"
NEWS_ENDPOINT = "https://newsapi.org/v2/everything"
stock_api_key = secret.stock_api_key
news_api = secret.news_api

account_sid = secret.account_sid
auth_token = secret.auth_token
from_number = "+16502521667"

stock_params = {
    "function": "TIME_SERIES_DAILY",
    "symbol": STOCK_NAME,
    "apikey": stock_api_key,

}

response = requests.get(STOCK_ENDPOINT, params=stock_params)
response.raise_for_status()
stock_data = response.json()["Time Series (Daily)"]

# Dictionary from json stock file
data_list = [value for (key, value) in stock_data.items()]
yesterday_data = data_list[0]
yesterday_closing_price = yesterday_data["4. close"]
print(yesterday_closing_price)
day_before_yester = data_list[1]
day_before_yester_close_price = day_before_yester["4. close"]
print(day_before_yester_close_price)

up_down = None
# Difference of yesterday(close) and day before yesterday(close)
difference = float(yesterday_closing_price) - float(day_before_yester_close_price)
if difference > 0:
    up_down = "📈"
else:
    up_down = "📉"

diff_percent = round((difference / float(yesterday_closing_price)) * 100, 2)
print(diff_percent)

if abs(diff_percent) > 5:
    print("Get News")

    # Find news articles
    news_params = {
        "apiKey": news_api,
        "qInTitle": COMPANY_NAME,
    }
    news_response = requests.get(url="https://newsapi.org/v2/everything", params=news_params)
    news_response.raise_for_status()
    articles = news_response.json()["articles"]
    print(articles[0]["title"])

    three_articles = articles[:3]
    print(three_articles)

    # Format articles and keep essential information
    formatted_articles = [
        f"{STOCK_NAME}: {up_down}{diff_percent}%\nHeadline: {article['title']}\nStory: {article['description']}" for
        article in three_articles]

    for i in formatted_articles:
        client = Client(account_sid, auth_token)
        message = client.messages \
            .create(
            body=i,
            from_=from_number,
            to=secret.my_number,
        )
        print(message.status)
