'''
import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "stocks_portfolio.settings")
import django
django.setup()
'''
from django.contrib.auth.models import AnonymousUser
from rest_framework import mixins
from rest_framework.response import Response
from rest_framework.views import APIView

from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.viewsets import ModelViewSet
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from stocks_app.models import Portfolio, StocksInPortfolio
from stocks_app.serializers import PortfolioSerializer, PortfolioListSerializer, \
    StocksInPortfolioSerializer, StocksInPortfolioListSerializer


class PortfolioView(ModelViewSet):
    """ портфель акций """
    queryset = Portfolio.objects.select_related('owner')
    serializer_class = PortfolioSerializer

    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filter_fields = ['name', 'owner', 'owner__username'] # /portfolio/?owner__username=test_user2
    search_fields = ['name', 'owner__username', 'owner__first_name', 'owner__last_name',
                     'owner__email'] # /portfolio/?search=petr
    ordering_fields = ['id', 'name', 'owner'] # /portfolio/?ordering=-owner

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
        #serializer.save(owner=self.request.user)

#    def perform_update(self, serializer):
        #serializer.save(owner=self.request.user)


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


'''
class CompanyListView(GenericViewSet, mixins.ListModelMixin):
    queryset = Company.objects \
        .filter(stockprice__is_actual=True, fundamentals__is_actual=True) \
        .values(
        'id', 'short_name', 'ticker', 'website',
        'industry__name',
        'stock_price__id', 'stock_price__price', 'stock_price__date_price', 'stock_price__currency__short_name',
        'fundamentals__financial_indicators', 'fundamentals__report_date', 'fundamentals__measure__short_name',
        'fundamentals__currency__short_name'
    )
    serializer_class = CompanyListSerializer
'''
'''
    def get(self, request):
        queryset = Company.objects \
            .filter(stock_price__is_actual=True, fundamentals__is_actual=True) \
            .values(
                'id', 'short_name', 'ticker', 'website',
                'industry__name',
                'stock_price__id', 'stock_price__price', 'stock_price__date_price', 'stock_price__currency__short_name',
                'fundamentals__financial_indicators', 'fundamentals__report_date', 'fundamentals__measure__short_name',
                'fundamentals__currency__short_name'
            )

        serializer_for_queryset = CompanyListSerializer(instance=queryset, many=True)
        return Response(serializer_for_queryset.data)
'''







'''
class CompanyListViewSet(ReadOnlyModelViewSet):
    queryset = Company.objects \
        .filter(stock_price__is_actual=True, fundamentals__is_actual=True) \
        .values(
        'id', 'short_name', 'ticker', 'website',
        'industry__name',
        'stock_price__id', 'stock_price__price', 'stock_price__date_price', 'stock_price__currency__short_name',
        'fundamentals__financial_indicators', 'fundamentals__report_date', 'fundamentals__measure__short_name',
        'fundamentals__currency__short_name'
    )

'''





