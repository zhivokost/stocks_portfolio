from django.contrib import admin
from .models import Industry, Country, Measure, Currency, Fundamentals, Stock_price, Company, Portfolio, Stock_portfolio

# Register your models here.

admin.site.register(Industry)
admin.site.register(Country)
admin.site.register(Measure)
admin.site.register(Currency)
admin.site.register(Fundamentals)
admin.site.register(Stock_price)
admin.site.register(Company)
admin.site.register(Portfolio)
admin.site.register(Stock_portfolio)
