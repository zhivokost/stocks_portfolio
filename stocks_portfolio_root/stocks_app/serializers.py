from django.contrib.auth.models import User
from rest_framework import serializers
from stocks_app.models import Portfolio, StocksInPortfolio, Company, Fundamentals, StockPrice, Industry, Country, \
    Measure, Currency


class UserSerializer(serializers.ModelSerializer):
    """ Сериализация пользователя """

    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'email']


class CurrencySerializer(serializers.ModelSerializer):
    """ Сериализация валюты """

    class Meta:
        model = Currency
        fields = ['short_name', 'full_name']


class MeasureSerializer(serializers.ModelSerializer):
    """ Сериализация меры измерения валюты (тыс., млн., млрд.) """

    class Meta:
        model = Measure
        fields = ['short_name', 'full_name']


class IndustrySerializer(serializers.ModelSerializer):
    """ Сериализация индустрии(отрасли) """

    class Meta:
        model = Industry
        fields = ['name', 'description']


class CountrySerializer(serializers.ModelSerializer):
    """ Сериализация сведений о стране """

    class Meta:
        model = Country
        fields = ['short_name', 'full_name']


class FundamentalsSerializer(serializers.ModelSerializer):
    """ Сериализация фундаментальных показателей компании """

    class Meta:
        model = Fundamentals
        exclude = ['company', 'created_at', 'updated_at']


class FundamentalsListSerializer(serializers.ModelSerializer):
    """ Сериализация фундаментальных показателей компании для просмотра """
    currency = CurrencySerializer(read_only=True)
    measure = MeasureSerializer(read_only=True)

    class Meta:
        model = Fundamentals
        fields = ['report_date', 'financial_indicators', 'currency', 'measure', 'public_date',
                  'source_site', 'next_public_date', 'is_actual']


class StockPriceSerializer(serializers.ModelSerializer):
    """ Сериализация цен на акции компании для просмотра """
    class Meta:
        model = StockPrice
        exclude = ['created_at', 'updated_at', 'company']


class StockPriceListSerializer(serializers.ModelSerializer):
    """ Сериализация цен на акции компании для просмотра """
    currency = CurrencySerializer(read_only=True)

    class Meta:
        model = StockPrice
        fields = ['price', 'currency', 'date_price']


class CompanySerializer(serializers.ModelSerializer):
    """ Сериализация сведений о компании """

    class Meta:
        model = Company
        exclude = ['created_at', 'updated_at']


class CompanyListSerializer(serializers.ModelSerializer):
    """ Сериализация сведений о компании для просмотра """
    company_fund = FundamentalsListSerializer(source='actual_fund', many=True, read_only=True, default=[])
    stock_price = StockPriceListSerializer(source='actual_stock_price', many=True, read_only=True, default=[])
    industry = IndustrySerializer(read_only=True)
    country = CountrySerializer(read_only=True)

    class Meta:
        model = Company
        fields = ['id', 'short_name', 'ticker', 'industry', 'company_fund',
                  'stock_price', 'full_name', 'website', 'country', 'description']


class PortfolioSerializer(serializers.ModelSerializer):
    """ Сериализация инвестиционного портфеля """

    class Meta:
        model = Portfolio
        fields = ['id', 'name', 'owner']


class PortfolioListSerializer(serializers.ModelSerializer):
    """ Сериализация для чтения списка портфелей """
    owner = UserSerializer(read_only=True)

    class Meta:
        model = Portfolio
        fields = ['id', 'name', 'owner']


class StocksInPortfolioSerializer(serializers.ModelSerializer):
    """ Сериализация списка компаний в портфеле """

    class Meta:
        model = StocksInPortfolio
        fields = ['id', 'company', 'stocks_count', 'invested_amount', 'buy_price', 'currency', 'portfolio_id']


class StocksInPortfolioListSerializer(serializers.ModelSerializer):
    """ Сериализация списка компаний в портфеле для просмотра """
    company = CompanySerializer(read_only=True)
    currency = CurrencySerializer(read_only=True)
    # company_id = serializers.IntegerField()
    # company_name = serializers.CharField(source='company__short_name')
    # ticker = serializers.CharField(source='company__ticker')
    # country = serializers.CharField(source='company__country__short_name')
    # currency = serializers.CharField(source='currency__short_name')

    class Meta:
        model = StocksInPortfolio
        fields = ['id', 'company', 'stocks_count', 'buy_price', 'invested_amount', 'currency']
