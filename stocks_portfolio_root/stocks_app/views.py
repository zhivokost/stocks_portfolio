from django.db.models import Prefetch
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.viewsets import ModelViewSet
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from stocks_app.models import Portfolio, StocksInPortfolio, Company, Fundamentals, StockPrice
from stocks_app.serializers import PortfolioSerializer, PortfolioListSerializer, \
    StocksInPortfolioSerializer, StocksInPortfolioListSerializer, CompanySerializer, CompanyListSerializer, \
    FundamentalsSerializer, FundamentalsListSerializer, StockPriceSerializer


class PortfolioView(ModelViewSet):
    """ портфель акций """
    queryset = Portfolio.objects.select_related('owner')
    serializer_class = PortfolioSerializer

    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filter_fields = ['name', 'owner', 'owner__username']  # /portfolio/?owner__username=test_user2
    search_fields = ['name', 'owner__username', 'owner__first_name', 'owner__last_name',
                     'owner__email']  # /portfolio/?search=petr
    ordering_fields = ['id', 'name', 'owner']  # /portfolio/?ordering=-owner

#    authentication_classes = [TokenAuthentication]
#    permission_classes = [IsAuthenticated]

#    def get_queryset(self):
#        return Portfolio.objects.filter(owner=self.request.user).select_related('owner')

    def list(self, request, *args, **kwargs):
        """ вывод списка портфелей пользователя """
        queryset = self.filter_queryset(self.queryset)
        serializer = PortfolioListSerializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, *args, **kwargs):
        """ вывод информации о конкретном портфеле пользователя """
        portfolio = get_object_or_404(self.queryset, pk=self.kwargs['pk'])
        serializer = PortfolioListSerializer(portfolio, many=False)
        return Response(serializer.data)

    def filter_queryset(self, queryset):
        """ фильтрация, поиск, сортировка """
        for backend in list(self.filter_backends):
            queryset = backend().filter_queryset(self.request, queryset, self)
        return queryset

#    def perform_create(self, serializer):
        # serializer.save(owner=self.request.user)

#    def perform_update(self, serializer):
        # serializer.save(owner=self.request.user)


class StocksInPortfolioView(ModelViewSet):
    """ компании (акции) в портфеле """
    serializer_class = StocksInPortfolioSerializer

    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filter_fields = ['company_id', 'company__short_name', 'company__ticker', 'company__country__short_name',
                     'currency__short_name', 'invested_amount']  # /stocks_in_portfolio/?company__ticker=RASP
    search_fields = ['company__short_name', 'company__ticker', 'company__country__short_name',
                     'currency__short_name']  # /stocks_in_portfolio/?search=Расп
    ordering_fields = ['company_id', 'company__short_name', 'company__ticker', 'company__country__short_name',
                       'currency__short_name', 'invested_amount']  # /stocks_in_portfolio/?ordering=-invested_amount

    def get_queryset(self):
        return StocksInPortfolio.objects.filter(portfolio_id=self.kwargs['id_portfolio'])

    def perform_create(self, serializer):
        serializer.save(portfolio_id=self.kwargs['id_portfolio'])

    def perform_update(self, serializer):
        serializer.save(portfolio_id=self.kwargs['id_portfolio'])

    def list(self, request, *args, **kwargs):
        """ вывод списка компании в конкретном портфеле """
        queryset = StocksInPortfolio.objects \
            .filter(portfolio_id=self.kwargs['id_portfolio']) \
            .values('company_id', 'company__short_name', 'company__ticker', 'company__country__short_name',
                    'stocks_count', 'buy_price', 'invested_amount', 'currency__short_name')
        queryset = self.filter_queryset(queryset)
        serializer = StocksInPortfolioListSerializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, *args, **kwargs):
        """ вывод информации о конкретной компании в конкретном портфеле """
        queryset = StocksInPortfolio.objects \
            .filter(portfolio_id=self.kwargs['id_portfolio']) \
            .values('company_id', 'company__short_name', 'company__ticker', 'company__country__short_name',
                    'stocks_count', 'buy_price', 'invested_amount', 'currency__short_name')
        company = get_object_or_404(queryset, pk=self.kwargs['pk'])
        serializer = StocksInPortfolioListSerializer(company, many=False)
        return Response(serializer.data)

    def filter_queryset(self, queryset):
        """ фильтрация, поиск, сортировка """
        for backend in list(self.filter_backends):
            queryset = backend().filter_queryset(self.request, queryset, self)
        return queryset


class CompanyView(ModelViewSet):
    """ Информация о компаниях (фирмах, организациях) """
    queryset = Company.objects.all()
    serializer_class = CompanySerializer

    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filter_fields = ['id', 'short_name', 'ticker', 'industry__name', 'company_fund__report_date',
                     'company_fund__public_date', 'full_name', 'website', 'country__short_name', 'country__full_name']
    # /companies/?short_name=ММК
    search_fields = ['short_name', 'ticker', 'industry__name', 'full_name', 'country__short_name', 'country__full_name']
    # /companies/?search=ит
    ordering_fields = ['id', 'short_name', 'ticker', 'industry__name', 'company_fund__report_date',
                       'company_fund__public_date', 'full_name', 'website', 'country__short_name', 'country__full_name',
                       'company_fund__financial_indicators__EBITDA']
    # /companies/?ordering=id

    def list(self, request, *args, **kwargs):
        """ вывод списка компаний """
        queryset = Company.objects.prefetch_related(Prefetch('company_fund', queryset=Fundamentals.objects
                                                             .filter(is_actual=True)
                                                             .select_related('measure', 'currency')
                                                             , to_attr='actual_fund'),
                                                    Prefetch('stock_price', queryset=StockPrice.objects
                                                             .filter(is_actual=True)
                                                             .select_related('currency')
                                                             , to_attr='actual_stock_price'))\
                                  .select_related('country', 'industry')
        queryset = self.filter_queryset(queryset)
        serializer = CompanyListSerializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, *args, **kwargs):
        """ вывод информации о конкретной компании"""
        queryset = Company.objects.prefetch_related(Prefetch('company_fund', queryset=Fundamentals.objects
                                                             .filter(is_actual=True)
                                                             .select_related('measure', 'currency')
                                                             , to_attr='actual_fund'),
                                                    Prefetch('stock_price', queryset=StockPrice.objects
                                                             .filter(is_actual=True)
                                                             .select_related('currency')
                                                             , to_attr='actual_stock_price')) \
                                  .select_related('country', 'industry')
        company = get_object_or_404(queryset, pk=self.kwargs['pk'])
        serializer = CompanyListSerializer(company, many=False)
        return Response(serializer.data)

    def filter_queryset(self, queryset):
        """ фильтрация, поиск, сортировка """
        for backend in list(self.filter_backends):
            queryset = backend().filter_queryset(self.request, queryset, self)
        return queryset


class FundamentalsView(ModelViewSet):
    """ фундаментальные показатели компании """
    serializer_class = FundamentalsSerializer

    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filter_fields = ['report_date', 'public_date', 'next_public_date', 'is_actual']
    # /fundamentals/?report_date=2021-12-31
    search_fields = ['report_date', 'public_date', 'next_public_date', 'is_actual']
    # /fundamentals/?search=2022-03
    ordering_fields = ['report_date', 'public_date', 'next_public_date', 'is_actual']
    # /fundamentals/?ordering=-is_actual

    def get_queryset(self):
        return Fundamentals.objects.filter(company_id=self.kwargs['id_company']).select_related('measure', 'currency')

    def perform_create(self, serializer):
        serializer.save(company_id=self.kwargs['id_company'])

    def perform_update(self, serializer):
        serializer.save(company_id=self.kwargs['id_company'])

    def list(self, request, *args, **kwargs):
        """ вывод списка фундаментальных показателей конкретной компании """
        queryset = Fundamentals.objects.filter(company_id=self.kwargs['id_company'])\
                               .select_related('measure', 'currency')
        queryset = self.filter_queryset(queryset)
        serializer = FundamentalsListSerializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, *args, **kwargs):
        """ вывод информации о фундаментальных показателях на конкретную дату конкретной компании """
        queryset = Fundamentals.objects.filter(company_id=self.kwargs['id_company'])\
                               .select_related('measure', 'currency')
        fundamentals = get_object_or_404(queryset, pk=self.kwargs['pk'])
        serializer = FundamentalsListSerializer(fundamentals, many=False)
        return Response(serializer.data)

    def filter_queryset(self, queryset):
        """ фильтрация, поиск, сортировка """
        for backend in list(self.filter_backends):
            queryset = backend().filter_queryset(self.request, queryset, self)
        return queryset


class StockPriceView(ModelViewSet):
    """ цены на акции компании """
    serializer_class = StockPriceSerializer

    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filter_fields = ['id', 'price', 'date_price', 'is_actual']
    # /stock_prices?is_actual=True
    search_fields = ['price', 'date_price', 'is_actual']
    # /stock_prices?search=2022-11-19 05:05
    ordering_fields = ['id', 'price', 'date_price', 'is_actual']
    # /stock_prices?ordering=-is_actual

    def get_queryset(self):
        return StockPrice.objects.filter(company_id=self.kwargs['id_company'])

    def perform_create(self, serializer):
        serializer.save(company_id=self.kwargs['id_company'])

    def perform_update(self, serializer):
        serializer.save(company_id=self.kwargs['id_company'])
