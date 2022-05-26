from .models import Portfolio, Company, Stock_portfolio
import requests

#import json


def view_list_of_portfolio(user_id):
    return Portfolio.objects\
        .filter(user_id=user_id)\
        .values('name', 'created_at')


def view_list_of_stocks_in_portfolio(portfolio_id):
    return Stock_portfolio.objects\
        .filter(portfolio_id=portfolio_id) \
        .values('company__short_name', 'stocks_count', 'buy_price', 'invested_amount',
                'currency__short_name', 'company__fundamentals__financial_indicators')
        #.prefetch_related('company', 'currency', 'fundamentals') \
        # .select_related('company', 'currency', 'fundamentals') \
        # .values('company__short_name', 'stocks_count', 'buy_price', 'invested_amount', 'currency__short_name')


def view_list_of_all_companies():
    return Company.objects\
        .values('short_name', 'country__short_name', 'industry__name', 'ticker', 'website',
                'fundamentals__financial_indicators', 'stock_price__price', 'stock_price__currency__short_name')


def load_stock_price_from_moex():
    try:
        url = 'https://iss.moex.com/iss/engines/stock/markets/shares/boards/TQBR/securities.json' \
              '?iss.meta=off&iss.only=marketdata&marketdata.columns=SECID,LAST,SYSTIME'
        r = requests.get(url)
        #r.encoding = 'utf-8'
        return r.json()
    except Exception as e:
        print(f'query error {str(e)}')
        return None

# services.load_stock_price_from_moexc()['marketdata']['data']