from django.shortcuts import render
from django.http import HttpResponse
from . import services

# Create your views here.


def portfolio_list(request):
    return render(request, './portfolio_info.html', {'portfolio_list': services.view_list_of_portfolio(1)})


def stocks_list_in_portfolio(request):
    return render(request, './stocks_info.html', {'stocks_list': services.view_list_of_stocks_in_portfolio(1)})
