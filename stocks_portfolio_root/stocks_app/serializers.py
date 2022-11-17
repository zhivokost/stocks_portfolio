import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "stocks_portfolio.settings")
import django
django.setup()


from copy import copy
from django.contrib.auth.models import User
from rest_framework import serializers, validators
from stocks_app.models import Portfolio, StocksInPortfolio


class UserSerializer(serializers.ModelSerializer):
    """ Сериализация пользователя """

    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'email']
'''
        extra_kwargs = {
            'username': {'validators': []},
        }

    def create(self, validated_data):
        user = User.objects.create(**validated_data)
        return user

    def update(self, instance, validated_data):
        instance.username = validated_data.get('username', instance.username)
        instance.save()
        return instance
'''


class PortfolioSerializer(serializers.ModelSerializer):
    """ Сериализация инвестиционного портфеля """

    class Meta:
        model = Portfolio
        fields = ['id', 'name', 'owner']

'''
    def create(self, validated_data):
        owner_data = validated_data.pop('owner')
        owner = User.objects.filter(username=owner_data.get('username')).first()
        if not owner:
            owner = UserSerializer.create(UserSerializer(), owner_data)
        portfolio = Portfolio.objects.create(owner=owner, **validated_data)
        return portfolio

    def update(self, instance, validated_data):
        if 'owner' in validated_data.keys():
            owner_data = validated_data.pop('owner')
            owner = User.objects.get(username=instance.owner.username)
            UserSerializer.update(UserSerializer(), owner, owner_data)
            instance.owner.username = owner_data.get('username', instance.owner.username)

        instance.name = validated_data.get('name', instance.name)
        instance.save()
        return instance
'''


class PortfolioListSerializer(serializers.ModelSerializer):
    """ Сериализация для чтения списка портфелей """
    owner = UserSerializer()

    class Meta:
        model = Portfolio
        fields = ['id', 'name', 'owner']


#queryset = Portfolio.objects.select_related('owner').values('id', 'name', 'owner__id', 'owner__username', 'owner__first_name', 'owner__last_name', 'owner__email')

#queryset = Portfolio.objects.select_related('owner')
#serializer = PortfolioListSerializer(queryset, many=True)
#serializer.data



#portfolio = Portfolio.objects.filter(id=3).first()
#serializer = PortfolioSerializer(portfolio, data={"name": "ИИС 5", "owner": {"username": "zhivokost5"}},
#                                partial=True)
#serializer = PortfolioSerializer(data={
#        "name": "ИИС 2",
#        "owner": {
#            "username": "zhivokost12"
#        }
#    })
#serializer.is_valid()
#serializer.save()


class StocksInPortfolioSerializer(serializers.ModelSerializer):
    """ Сериализация списка компаний в портфеле """

    class Meta:
        model = StocksInPortfolio
        fields = ['id', 'company', 'stocks_count', 'invested_amount', 'buy_price', 'currency', 'portfolio_id']


class StocksInPortfolioListSerializer(serializers.ModelSerializer):
    company_id = serializers.IntegerField()
    company_name = serializers.CharField(source='company__short_name')
    ticker = serializers.CharField(source='company__ticker')
    country = serializers.CharField(source='company__country__short_name')
    currency = serializers.CharField(source='currency__short_name')

    class Meta:
        model = StocksInPortfolio
        #fields = ['company', 'company_name', 'ticker', 'country', 'currency']
        exclude = ['created_at', 'updated_at', 'portfolio', 'company']

'''
class CompanyListSerializer(serializers.ModelSerializer):
#    id = serializers.IntegerField()
#    company = serializers.CharField(source='short_name')
#    ticker = serializers.CharField()
#    site = serializers.URLField(source='website')
    industry = serializers.CharField(source='industry__name')
    price = serializers.FloatField(source='stock_price__price')
    price_currency = serializers.CharField(source='stock_price__currency__short_name')
    price_date = serializers.DateTimeField(source='stock_price__date_price')
    fin_indicators = serializers.JSONField(source='fundamentals__financial_indicators')
    fin_measure = serializers.CharField(source='fundamentals__measure__short_name')
    fin_currency = serializers.CharField(source='fundamentals__currency__short_name')
    fin_report_date = serializers.DateField(source='fundamentals__report_date')

    class Meta:
        model = Company
        exclude = ['full_name', 'description', 'created_at', 'updated_at', 'country']
'''


















'''
class StockPriceSerializer(ModelSerializer):
    #currency = serializers.CharField(source='currency.short_name', default='', read_only=True)

    class Meta:
        model = StockPrice
        fields = '__all__' #['price', 'currency', 'date_price']


class FundamentalsSerializer(ModelSerializer):
    currency = serializers.CharField(source='currency.short_name', default='', read_only=True)
    measure = serializers.CharField(source='measure.short_name', default='', read_only=True)

    class Meta:
        model = Fundamentals
        fields = ['financial_indicators', 'measure', 'currency', 'report_date', 'source_site']

'''
'''
class CompanySerializer(ModelSerializer):
    class Meta:
        model = Company
        fields = ['stock_price']
        #depth = 1
    #industry = serializers.CharField(source='industry.name', default='', read_only=True)
    #fundamentals = serializers.PrimaryKeyRelatedField(many=True, queryset=Fundamentals.objects.all())
    #fundamentals = serializers.SlugRelatedField(many=True, slug_field='financial_indicators', read_only=True)
    #stock_price = serializers.SlugRelatedField(many=True, read_only=True, slug_field='price')
    #stock_price = StockPriceSerializer(default='', read_only=True, many=True)
    #fundamentals = FundamentalsSerializer(default='', read_only=True, many=True)
    #stock_price = serializers.SerializerMethodField()
    #fundamentals = serializers.SerializerMethodField()
    #stock_price = StockPriceListField(many=True, read_only=True)
                                      #queryset=Stock_price.objects.all().select_related('currency', 'company'))

'''

'''
    def get_stock_price(self, company):
        stock_price = Stock_price.objects.filter(company_id=company, is_actual=True).select_related('currency')
        serializer = StockPriceSerializer(instance=stock_price, many=True)
        return serializer.data
'''
'''
    def get_fundamentals(self, company):
        fundamentals = Fundamentals.objects.filter(company_id=company, is_actual=True)
        serializer = FundamentalsSerializer(instance=fundamentals, many=True)
        return serializer.data
'''



