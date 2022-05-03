from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Industry(models.Model):
    """ Отрасль (индустрия) """

    class Meta:
        db_table = 'Industry'
        verbose_name = 'Отрасль'

    name = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return f'{self.name}'


class Country(models.Model):
    """ Страна """

    class Meta:
        db_table = 'Country'
        verbose_name = 'Страна'

    short_name = models.CharField(max_length=100)
    full_name = models.CharField(max_length=250, blank=True, null=True)

    def __str__(self):
        return f'{self.short_name}'


class Measure(models.Model):
    """ Мера измерения (тыс., млн., млрд.) """

    class Meta:
        db_table = 'Measure'
        verbose_name = 'Мера измерения'

    short_name = models.CharField(max_length=50)
    full_name = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return f'{self.short_name}'


class Currency(models.Model):
    """ Валюта """

    class Meta:
        db_table = 'Currency'
        verbose_name = 'Валюта'

    short_name = models.CharField(max_length=50)
    full_name = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return f'{self.short_name}'


class Fundamentals(models.Model):
    """ Фундаментальные показатели компании """

    class Meta:
        db_table = 'Fundamentals'
        verbose_name = 'Фундаментальные показатели компании'
        ordering = ['is_actual']

    financial_indicators = models.JSONField()
    measure = models.ForeignKey(Measure, on_delete=models.SET_NULL, null=True)
    currency = models.ForeignKey(Currency, on_delete=models.SET_NULL, null=True)
    report_date = models.DateField()
    is_actual = models.BooleanField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True, null=True)
    next_report_date = models.DateField()
    source_site = models.URLField()


class Stock_price(models.Model):
    """ Цена акции компании """

    class Meta:
        db_table = 'Stock_price'
        verbose_name = 'Цена акции компании'
        ordering = ['is_actual']

    price = models.FloatField()
    currency = models.ForeignKey(Currency, on_delete=models.SET_NULL, null=True)
    date_price = models.DateField()
    is_actual = models.BooleanField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True, null=True)


class Company(models.Model):
    """ Информация о компании """

    class Meta:
        db_table = 'Company'
        verbose_name = 'Информация о компании'
        ordering = ['created_at']

    short_name = models.CharField(max_length=200)
    full_name = models.TextField(blank=True, null=True)
    tiker = models.CharField(max_length=20)
    website = models.URLField()
    industry = models.ForeignKey(Industry, on_delete=models.SET_NULL, null=True)
    country = models.ForeignKey(Country, on_delete=models.SET_NULL, null=True)
    stock_price = models.ForeignKey(Stock_price, on_delete=models.SET_NULL, null=True)
    fundamentals = models.ForeignKey(Fundamentals, on_delete=models.SET_NULL, null=True)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True, null=True)

    def __str__(self):
        return f'{self.short_name}'


class Portfolio(models.Model):
    """ Инвестиционный портфель (счет) """

    class Meta:
        db_table = 'Portfolio'
        verbose_name = 'Инвестиционный портфель'

    name = models.CharField(max_length=200)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.name}'


class Stock_portfolio(models.Model):
    """ Акции компании в портфеле """

    class Meta:
        db_table = 'Stock_portfolio'
        verbose_name = 'Акции компании в портфеле'
        ordering = ['company']

    portfolio = models.ForeignKey(Portfolio, on_delete=models.SET_NULL, null=True)
    company = models.ForeignKey(Company, on_delete=models.SET_NULL, null=True)
    invested_amount = models.FloatField()
    measure = models.ForeignKey(Measure, on_delete=models.SET_NULL, null=True)
    currency = models.ForeignKey(Currency, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True, null=True)
