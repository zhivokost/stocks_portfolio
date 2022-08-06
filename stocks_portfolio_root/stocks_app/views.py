import os
import django
from rest_framework.response import Response
from rest_framework.views import APIView

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "stocks_portfolio.settings")
django.setup()
from django.shortcuts import render
from django.http import HttpResponse
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.viewsets import ModelViewSet

from stocks_app.models import Company
from stocks_app.serializers import CompanySerializer, CompSerializer


class CompanyViewSet(ModelViewSet):
    queryset = Company.objects.all().select_related('industry').prefetch_related('stock_price', 'fundamentals')
        #values('short_name', 'ticker', 'website', 'industry__name')
    #queryset = Company.objects.select_related('industry').prefetch_related('stock_price', 'fundamentals').values('short_name', 'ticker', 'website', 'industry__name', 'stock_price__price')
    serializer_class = CompanySerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filter_fields = ['short_name', 'full_name', 'ticker']  # /company/?short_name='Новатэк'
    search_fields = ['short_name', 'full_name', 'ticker']  # /company/?search=Новатэк
    ordering_fields = ['industry', 'country', 'updated_at']  # /company/?ordering=-updated_at


class GetCompanyInfoView(APIView):
    def get(self, request):

        queryset = Company.objects \
            .filter(stock_price__is_actual=True, fundamentals__is_actual=True) \
            .values(
            'short_name', 'ticker', 'website',
            'industry__name',
            'stock_price__price', 'stock_price__date_price', 'stock_price__currency__short_name',
            'fundamentals__financial_indicators', 'fundamentals__report_date', 'fundamentals__measure__short_name',
            'fundamentals__currency__short_name'
            )

        serializer_for_queryset = CompSerializer(instance=queryset, many=True)
        return Response(serializer_for_queryset.data)
