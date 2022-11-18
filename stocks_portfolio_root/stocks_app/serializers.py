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
    currency = CurrencySerializer(read_only=True)
    measure = MeasureSerializer(read_only=True)

    class Meta:
        model = Fundamentals
        fields = ['report_date', 'financial_indicators', 'currency', 'measure', 'public_date',
                  'source_site', 'next_public_date']


class StockPriceSerializer(serializers.ModelSerializer):
    """ Сериализация цен на акции компании """

    class Meta:
        model = StockPrice
        fields = '__all__'


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
    owner = UserSerializer(read_only=True)

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
    """ Сериализация списка компаний в портфеле для просмотра """
    company_id = serializers.IntegerField()
    company_name = serializers.CharField(source='company__short_name')
    ticker = serializers.CharField(source='company__ticker')
    country = serializers.CharField(source='company__country__short_name')
    currency = serializers.CharField(source='currency__short_name')

    class Meta:
        model = StocksInPortfolio
        exclude = ['created_at', 'updated_at', 'portfolio', 'company']


class CompanySerializer(serializers.ModelSerializer):
    """ Сериализация сведений о компании """

    class Meta:
        model = Company
        exclude = ['created_at', 'updated_at']


class CompanyListSerializer(serializers.ModelSerializer):
    """ Сериализация сведений о компании для просмотра """
    company_fund = FundamentalsSerializer(source='actual_fund', many=True, read_only=True)
    stock_price = StockPriceSerializer(source='actual_stock_price', many=True, read_only=True)
    industry = IndustrySerializer(read_only=True)
    country = CountrySerializer(read_only=True)

    class Meta:
        model = Company
        fields = ['id', 'short_name', 'ticker', 'industry', 'company_fund',
                  'stock_price', 'full_name', 'website', 'country', 'description']


















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



