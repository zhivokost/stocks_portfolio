from django.shortcuts import render
from django.http import HttpResponse
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.viewsets import ModelViewSet

from stocks_app import services
from stocks_app.models import Company
from stocks_app.serializers import CompanySerializer


def portfolio_list(request):
    return render(request, './portfolio_info.html', {'portfolio_list': services.view_list_of_portfolio(1)})


def stocks_list_in_portfolio(request):
    queryset = services.view_list_of_stocks_in_portfolio(1)
    #queryset.
    return render(request, './stocks_info.html', {'stocks_list': queryset})


def search_companies(request):
    queryset = services.view_list_of_all_companies()
    #queryset.
    return render(request, './search_companies.html', {'companies_list': queryset})


class CompanyViewSet(ModelViewSet):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filter_fields = ['short_name', 'full_name', 'ticker']  # /company/?short_name='Новатэк'
    search_fields = ['short_name', 'full_name', 'ticker']  # /company/?search=Новатэк
    ordering_fields = ['industry', 'country', 'updated_at'] # /company/?ordering=-updated_at

