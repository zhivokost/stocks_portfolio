from django.contrib import admin
from .models import Industry, Country, Measure, Currency, Fundamentals, StockPrice, Company, Portfolio, StocksInPortfolio

# Register your models here.

admin.site.register(Industry)
admin.site.register(Country)
admin.site.register(Measure)
admin.site.register(Currency)
admin.site.register(Fundamentals)
admin.site.register(StockPrice)
admin.site.register(Company)
admin.site.register(Portfolio)
admin.site.register(StocksInPortfolio)
