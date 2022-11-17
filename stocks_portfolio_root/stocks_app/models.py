from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Industry(models.Model):
    """ Отрасль (индустрия) """

    class Meta:
        db_table = 'Industry'
        verbose_name = 'Отрасль'
        verbose_name_plural = 'Отрасли'

    name = models.CharField(max_length=100, verbose_name='Название отрасли', unique=True)
    description = models.TextField(blank=True, null=True, verbose_name='Описание')

    def __str__(self):
        return f'{self.name}'


class Country(models.Model):
    """ Страна """

    class Meta:
        db_table = 'Country'
        verbose_name = 'Страна'
        verbose_name_plural = 'Страны'

    short_name = models.CharField(max_length=50, verbose_name='Краткое название страны', unique=True)
    full_name = models.CharField(max_length=200, blank=True, null=True, verbose_name='Полное наименование')

    def __str__(self):
        return f'{self.short_name}'


class Measure(models.Model):
    """ Мера измерения (тыс., млн., млрд.) """

    class Meta:
        db_table = 'Measure'
        verbose_name = 'Мера измерения'
        verbose_name_plural = 'Меры измерения'

    short_name = models.CharField(max_length=10, verbose_name='Сокращенное название меры', unique=True)
    full_name = models.CharField(max_length=60, blank=True, null=True, verbose_name='Полное название')

    def __str__(self):
        return f'{self.short_name}'


class Currency(models.Model):
    """ Валюта """

    class Meta:
        db_table = 'Currency'
        verbose_name = 'Валюта'
        verbose_name_plural = 'Валюты'
        ordering = ['short_name']

    short_name = models.CharField(max_length=10, verbose_name='Скоращенное название валюты', unique=True)
    full_name = models.CharField(max_length=60, blank=True, null=True, verbose_name='Полное наименование')

    def __str__(self):
        return f'{self.short_name}'


class Company(models.Model):
    """ Информация о компании """

    class Meta:
        db_table = 'Company'
        verbose_name = 'Информация о компании'
        verbose_name_plural = 'Информация о компаниях'
        ordering = ['short_name']

    short_name = models.CharField(max_length=100, verbose_name='Краткое наименование')
    full_name = models.CharField(max_length=250, blank=True, null=True, verbose_name='Полное')
    ticker = models.CharField(max_length=10, verbose_name='Тикер акции', unique=True)
    website = models.URLField(verbose_name='Сайт компании')
    industry = models.ForeignKey(Industry, on_delete=models.SET_NULL, blank=True, null=True, verbose_name='Отрасль',
                                 related_name='company_industry')
    country = models.ForeignKey(Country, on_delete=models.SET_NULL, blank=True, null=True, verbose_name='Страна',
                                related_name='company_country')
    description = models.TextField(blank=True, null=True, verbose_name='Описание')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Создано')
    updated_at = models.DateTimeField(auto_now=True, blank=True, null=True, verbose_name='Изменено')

    def __str__(self):
        return f'{self.short_name}'


class Fundamentals(models.Model):
    """ Фундаментальные показатели компании """

    class Meta:
        db_table = 'Fundamentals'
        verbose_name = 'Фундаментальные показатели компании'
        verbose_name_plural = 'Фундаментальные показатели компании'
        ordering = ['is_actual']
        unique_together = ['financial_indicators', 'report_date']

    company = models.ForeignKey(Company, on_delete=models.SET_NULL, null=True, verbose_name='Компания',
                                related_name='company_fund')
    financial_indicators = models.JSONField(verbose_name='Финансовые показатели')
    measure = models.ForeignKey(Measure, on_delete=models.SET_NULL, blank=True, null=True, verbose_name='Измерение в',
                                related_name='fin_measure')
    currency = models.ForeignKey(Currency, on_delete=models.SET_NULL, null=True, verbose_name='Валюта',
                                 related_name='fin_currency')
    report_date = models.DateField(null=True, verbose_name='Отчетная дата')
    public_date = models.DateField(blank=True, null=True, verbose_name='Дата публикации отчета')
    is_actual = models.BooleanField(verbose_name='Актуальный?', default=False)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Создано')
    updated_at = models.DateTimeField(auto_now=True, null=True, verbose_name='Изменено')
    next_public_date = models.DateField(blank=True, null=True, verbose_name='Дата публикации следующего отчета')
    source_site = models.URLField(blank=True, null=True, verbose_name='Источник сведений о фин. показателях')

    def __str__(self):
        return f'{self.company}, {self.report_date}'


class StockPrice(models.Model):
    """ Цена акции компании """

    class Meta:
        db_table = 'Stock_prices'
        verbose_name = 'Цена акции компании'
        verbose_name_plural = 'Цены акции компании'
        ordering = ['is_actual']

    company = models.ForeignKey(Company, on_delete=models.SET_NULL, null=True, verbose_name='Компания',
                                related_name='stock_price')
    price = models.FloatField(verbose_name='Цена акции')
    currency = models.ForeignKey(Currency, on_delete=models.SET_NULL, null=True, verbose_name='Валюта',
                                 related_name='price_curr')
    date_price = models.DateTimeField(verbose_name='Цена на дату')
    is_actual = models.BooleanField(verbose_name='Актуальная?', default=False)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Создано')
    updated_at = models.DateTimeField(auto_now=True, blank=True, null=True, verbose_name='Изменено')

    def __str__(self):
        return f'{self.company}'


class Portfolio(models.Model):
    """ Инвестиционный портфель (счет) """

    class Meta:
        db_table = 'Portfolio'
        verbose_name = 'Инвестиционный портфель'
        verbose_name_plural = 'Инвестиционные портфели'
        unique_together = ['name', 'owner']

    name = models.CharField(max_length=100, verbose_name='Название портфеля')
    owner = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True, verbose_name='Владелец',
                              related_name='owner')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Создано')

    def __str__(self):
        return f'{self.name}'


class StocksInPortfolio(models.Model):
    """ Акции компании в портфеле """

    class Meta:
        db_table = 'Stocks_portfolio'
        verbose_name = 'Акции компаний в портфеле'
        verbose_name_plural = 'Акции компаний в портфеле'
        ordering = ['company']
        unique_together = ['portfolio', 'company']

    portfolio = models.ForeignKey(Portfolio, on_delete=models.SET_NULL, blank=True, null=True, verbose_name='Портфель',
                                  related_name='portfolio')
    company = models.ForeignKey(Company, on_delete=models.SET_NULL, blank=True, null=True, verbose_name='Компания',
                                related_name='company_in_portfolio')
    stocks_count = models.IntegerField(verbose_name='Количество акций', null=True)
    buy_price = models.FloatField(verbose_name='Цена покупки', null=True)
    invested_amount = models.FloatField(verbose_name='Сумма инвестиций', null=True)
    currency = models.ForeignKey(Currency, on_delete=models.SET_NULL, blank=True, null=True, verbose_name='Валюта',
                                 related_name='portfolio_curr')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Создано')
    updated_at = models.DateTimeField(auto_now=True, blank=True, null=True, verbose_name='Изменено')

    def __str__(self):
        return f'{self.company}'
