import os
import django
import pytz

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "stocks_portfolio.settings")
django.setup()

from stocks_app.models import Portfolio, Company, Stock_portfolio, Stock_price
from django.db.models import Max
import datetime
from django.utils.timezone import make_aware

import requests

# import json


def view_list_of_portfolio(user_id):
    return Portfolio.objects\
        .filter(user_id=user_id)\
        .values('name', 'created_at')


def view_list_of_stocks_in_portfolio(portfolio_id):
    return Stock_portfolio.objects\
        .filter(portfolio_id=portfolio_id) \
        .values('company__short_name', 'stocks_count', 'buy_price', 'invested_amount',
                'currency__short_name', 'company__fundamentals__financial_indicators')
        # prefetch_related('company', 'currency', 'fundamentals') \
        # select_related('company', 'currency', 'fundamentals') \
        # values('company__short_name', 'stocks_count', 'buy_price', 'invested_amount', 'currency__short_name')


def view_list_of_all_companies():
    return Company.objects\
        .values('short_name', 'country__short_name', 'industry__name', 'ticker', 'website',
                'fundamentals__financial_indicators', 'stock_price__price', 'stock_price__currency__short_name')


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
                Stock_price.objects.create(company_id=company.get('id'),
                                           price=ticker_price[1],
                                           currency_id=currency,
                                           date_price=make_aware(datetime.datetime.strptime(ticker_price[2], "%Y-%m-%d %H:%M:%S"), tz))
                # insert into table of stock prices with actual prices
                # in database will work trigger on insert, update and delete
                print(company.get('id'), ticker_price[1],
                      make_aware(datetime.datetime.strptime(ticker_price[2], "%Y-%m-%d %H:%M:%S"), tz))
                break




update_stock_prices()