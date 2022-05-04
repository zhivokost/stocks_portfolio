from .models import Industry, Country, Measure, Currency, Fundamentals, Stock_price, Company, Portfolio, Stock_portfolio


def view_list_of_portfolio(user_id):
    return Portfolio.objects\
        .filter(user_id=user_id)\
        .values('name', 'created_at')


def view_list_of_stocks_in_portfolio(portfolio_id):
    return Stock_portfolio.objects\
        .filter(portfolio_id=portfolio_id)\
        .select_related('company', 'currency')\
        .values('company__short_name', 'invested_amount', 'currency__short_name')
