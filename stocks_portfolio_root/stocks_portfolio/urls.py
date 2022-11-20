"""stocks_portfolio URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.contrib import admin
from django.urls import include, path, re_path
from rest_framework.routers import SimpleRouter

from stocks_app.views import PortfolioView, StocksInPortfolioView, CompanyView, FundamentalsView, StockPriceView

router = SimpleRouter()
router.register('portfolio', PortfolioView, basename='portfolio')
router.register('portfolio/(?P<id_portfolio>[^/.]+)/stocks_in_portfolio', StocksInPortfolioView, basename='stocks_portfolio')
router.register('companies', CompanyView, basename='companies')
router.register('companies/(?P<id_company>[^/.]+)/fundamentals', FundamentalsView, basename='fundamentals')
router.register('companies/(?P<id_company>[^/.]+)/stock_prices', StockPriceView, basename='stock_prices')


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/auth/', include('djoser.urls')),
    re_path(r'^auth/', include('djoser.urls.authtoken')),
    path('api/', include(router.urls)),

]

if settings.DEBUG:
    urlpatterns = [path('__debug__/', include('debug_toolbar.urls'))] + urlpatterns
