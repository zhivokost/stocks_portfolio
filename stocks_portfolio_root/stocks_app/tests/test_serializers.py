import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "stocks_portfolio.settings")

import django
django.setup()

from django.contrib.auth.models import User

import datetime

from django.test import TestCase

from stocks_app.models import Company, Industry, Fundamentals, Portfolio
from stocks_app.serializers import PortfolioSerializer, UserSerializer



class PortfolioSerializerTestCase(TestCase):
    def setUp(self):
        self.data = {"name": "ИИС 3", "owner": {"username": "zhivokost133"}}

    def test_create(self):
        serializer = PortfolioSerializer(data=self.data)
        serializer.is_valid()
        serializer.save()
        self.assertEqual(True, serializer.is_valid())



class CompanySerializerTestCase(TestCase):
    def test_ok(self):
        industry_1 = Industry.objects.create(name='industry 1')
        industry_2 = Industry.objects.create(name='industry 2')
        company_1 = Company.objects.create(short_name='Test name 1', ticker='ticker 1', website='website 1', industry=industry_1)
        company_2 = Company.objects.create(short_name='Test name 2', ticker='ticker 2', website='website 2', industry=industry_2)
        Stock_price.objects.create(company=company_1, price=1000, date_price=datetime.date(2022, 1, 3), is_actual=True)
        Stock_price.objects.create(company=company_2, price=1025.47, date_price=datetime.date(2022, 2, 22), is_actual=True)
        Fundamentals.objects.create(company=company_1, financial_indicators={"EBITDA": '500000', "Выручка": '600000'}, is_actual=True)
        Fundamentals.objects.create(company=company_2, financial_indicators={"EBITDA": '400000', "Выручка": '500000'}, is_actual=True)

        data = CompanySerializer([company_1, company_2], many=True).data
        print(data)
        expected_data = [
            {
                'id': company_1.id,
                'short_name': 'Test name 1',
                'ticker': 'ticker 1',
                'website': 'website 1',
                'industry': 'industry 1',
                'stock_price': [1000.0],
                'fundamentals': [{"EBITDA": '500000', "Выручка": '600000'}]
            },
            {
                'id': company_2.id,
                'short_name': 'Test name 2',
                'ticker': 'ticker 2',
                'website': 'website 2',
                'industry': 'industry 2',
                'stock_price': [1025.47],
                'fundamentals': [{"EBITDA": '400000', "Выручка": '500000'}]
            }
        ]
        #print(expected_data)
        self.assertEqual(expected_data, data)
