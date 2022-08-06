import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "stocks_portfolio.settings")
django.setup()

from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from stocks_app.models import Company, Stock_price, Fundamentals


class StockPriceSerializer(ModelSerializer):
    currency = serializers.CharField(source='currency.short_name', default='', read_only=True)

    class Meta:
        model = Stock_price
        fields = ['price', 'currency', 'date_price']


class FundamentalsSerializer(ModelSerializer):
    currency = serializers.CharField(source='currency.short_name', default='', read_only=True)
    measure = serializers.CharField(source='measure.short_name', default='', read_only=True)

    class Meta:
        model = Fundamentals
        fields = ['financial_indicators', 'measure', 'currency', 'report_date', 'source_site']


class CompanySerializer(ModelSerializer):
    industry = serializers.CharField(source='industry.name', default='', read_only=True)
    #fundamentals = serializers.PrimaryKeyRelatedField(many=True, queryset=Fundamentals.objects.all())
    #fundamentals = serializers.SlugRelatedField(many=True, slug_field='financial_indicators', read_only=True)
    #stock_price = serializers.SlugRelatedField(many=True, read_only=True, slug_field='price')
    #stock_price = StockPriceSerializer(default='', read_only=True, many=True)
    #fundamentals = FundamentalsSerializer(default='', read_only=True, many=True)
    stock_price = serializers.SerializerMethodField()
    #fundamentals = serializers.SerializerMethodField()
    #stock_price = StockPriceListField(many=True, read_only=True)
                                      #queryset=Stock_price.objects.all().select_related('currency', 'company'))

    class Meta:
        model = Company
        fields = ['id', 'short_name', 'ticker', 'website', 'industry', 'stock_price', 'fundamentals']

    def get_stock_price(self, company):
        stock_price = Stock_price.objects.filter(company_id=company, is_actual=True).select_related('currency')
        serializer = StockPriceSerializer(instance=stock_price, many=True)
        return serializer.data
'''
    def get_fundamentals(self, company):
        fundamentals = Fundamentals.objects.filter(company_id=company, is_actual=True)
        serializer = FundamentalsSerializer(instance=fundamentals, many=True)
        return serializer.data
'''


class CompSerializer(serializers.Serializer):
    company = serializers.CharField(source='short_name', max_length=100)
    ticker = serializers.CharField(max_length=10)
    site = serializers.URLField(source='website')
    industry = serializers.CharField(source='industry__name', max_length=100)
    price = serializers.FloatField(source='stock_price__price')
    price_currency = serializers.CharField(source='stock_price__currency__short_name', max_length=10)
    price_date = serializers.DateTimeField(source='stock_price__date_price')
    fin_indicators = serializers.JSONField(source='fundamentals__financial_indicators')
    fin_measure = serializers.CharField(source='fundamentals__measure__short_name', max_length=10)
    fin_currency = serializers.CharField(source='fundamentals__currency__short_name', max_length=10)
    fin_report_date = serializers.DateField(source='fundamentals__report_date')
