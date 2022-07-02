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


class StockPriceListField(serializers.RelatedField):
    def to_representation(self, value):
        return f'{value.price, value.currency, value.date_price}'


class FundamentalsRelatedField(serializers.SlugRelatedField):
    def get_queryset(self):
        queryset = Fundamentals.objects.filter(is_actual=True)
        return queryset


class CompanySerializer(ModelSerializer):
    industry = serializers.CharField(source='industry.name', default='', read_only=True)
    #fundamentals = serializers.PrimaryKeyRelatedField(many=True, queryset=Fundamentals.objects.all())
    fundamentals = serializers.SlugRelatedField(many=True, slug_field='financial_indicators', queryset=Fundamentals.objects.filter(is_actual=True))
    stock_price = serializers.SlugRelatedField(many=True, read_only=True, slug_field='price')
    #stock_price = StockPriceSerializer(source='stock_price_set', default='', read_only=True, many=True)
    #stock_price = StockPriceListField(many=True, read_only=True)
                                      #queryset=Stock_price.objects.all().select_related('currency', 'company'))

    class Meta:
        model = Company
        fields = ['id', 'short_name', 'ticker', 'website', 'industry', 'stock_price', 'fundamentals']
