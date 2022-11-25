import pytz
from stocks_app.models import Company, StockPrice
import datetime
from django.utils.timezone import make_aware
import requests
import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "stocks_portfolio.settings")
django.setup()


def load_stock_price_from_moex():
    try:
        url = 'https://iss.moex.com/iss/engines/stock/markets/shares/boards/TQBR/securities.json' \
              '?iss.meta=off&iss.only=marketdata&marketdata.columns=SECID,LAST,SYSTIME'
        r = requests.get(url)
        # r.encoding = 'utf-8'
        return r.json()['marketdata']['data']
    except Exception as e:
        print(f'query error {str(e)}')
        return None


def update_stock_prices():
    companies = Company.objects.values('id', 'ticker').filter(country_id=1)  # select all companies from Russia
    # print(companies)
    actual_prices = load_stock_price_from_moex()  # load actual info of stocks from MOEX
    # print(actual_prices)
    tz = pytz.timezone('Europe/Moscow')  # MOEX work on Moscow timezone
    currency = 1  # russian ruble
    for company in companies:
        for ticker_price in actual_prices:
            if company.get('ticker') == ticker_price[0]:
                StockPrice.objects.create(company_id=company.get('id'),
                                          price=ticker_price[1],
                                          currency_id=currency,
                                          date_price=make_aware(datetime.datetime.strptime(ticker_price[2],
                                                                                           "%Y-%m-%d %H:%M:%S"), tz))
                # insert into table of stock prices with actual prices
                # in database will work trigger on insert, update and delete
                print(company.get('id'), ticker_price[1],
                      make_aware(datetime.datetime.strptime(ticker_price[2], "%Y-%m-%d %H:%M:%S"), tz))
                break


#  update_stock_prices()
