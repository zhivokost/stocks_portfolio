from .models import Company, Portfolio, Stock_portfolio


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
