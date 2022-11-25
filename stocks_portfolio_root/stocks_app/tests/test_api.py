from django.contrib.auth.models import User
from django.utils.datetime_safe import strftime

from stocks_app.serializers import PortfolioListSerializer, PortfolioSerializer, StocksInPortfolioListSerializer, \
    StocksInPortfolioSerializer, CompanyListSerializer, CompanySerializer, FundamentalsListSerializer, \
    FundamentalsSerializer, StockPriceSerializer
import json
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from stocks_app.models import Company, Portfolio, StocksInPortfolio, Industry, Country, Measure, Currency, \
    Fundamentals, StockPrice


class UserAuthTestCase(APITestCase):
    """ тесты API аутентификации и авторизации пользователя """
    def setUp(self):
        """ user create """
        url = reverse('user-list')
        self.user_data = {"username": "test_user", "password": "test_password",
                          "first_name": "test2", "last_name": "test1", "email": "test_user@gmail.com"}
        self.user = self.client.post(url, data=json.dumps(self.user_data), content_type='application/json')
        """ create token for new user """
        url = reverse('login')
        login_data = {"username": self.user_data['username'], "password": self.user_data['password']}
        self.token = self.client.post(url, data=json.dumps(login_data), content_type='application/json')

    def test_create_and_delete(self):
        """ user create """
        url = reverse('user-list')
        user_data = {"username": "user1", "password": "test1_password", "first_name": "test2", "last_name": "test1",
                     "email": "user1@gmail.com"}
        user = self.client.post(url, data=json.dumps(user_data), content_type='application/json')
        self.assertEqual(status.HTTP_201_CREATED, user.status_code)
        """ create token for new user """
        url = reverse('login')
        login_data = {"username": user_data['username'], "password": user_data['password']}
        token = self.client.post(url, data=json.dumps(login_data), content_type='application/json')
        self.assertEqual(status.HTTP_200_OK, token.status_code)

        """ token delete """
        url = reverse('logout')
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.data.get('auth_token'))
        response = self.client.post(url)
        self.assertEqual(status.HTTP_204_NO_CONTENT, response.status_code)

        """ user delete """
        url = reverse('login')
        login_data = {"username": user_data['username'], "password": user_data['password']}
        self.client.credentials()
        token = self.client.post(url, data=json.dumps(login_data), content_type='application/json')

        url = reverse('user-detail', args=['me'])
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.data.get('auth_token'))
        data = {"current_password": user_data['password']}
        response = self.client.delete(url, data=json.dumps(data), content_type='application/json')
        self.assertEqual(status.HTTP_204_NO_CONTENT, response.status_code)

    def test_get(self):
        url = reverse('user-detail', args=['me'])
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.data.get('auth_token'))
        response = self.client.get(url)
        self.assertEqual(status.HTTP_200_OK, response.status_code)

    def test_set_username(self):
        url = reverse('user-detail', args=['set_username'])
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.data.get('auth_token'))
        data = {"new_username": "user1", "current_password": self.user_data['password']}
        response = self.client.post(url, data=json.dumps(data), content_type='application/json')
        self.assertEqual(status.HTTP_204_NO_CONTENT, response.status_code)

        url = reverse('login')
        login_data = {"username": data['new_username'], "password": self.user_data['password']}
        response = self.client.post(url, data=json.dumps(login_data), content_type='application/json')
        self.assertEqual(status.HTTP_200_OK, response.status_code)

    def test_set_password(self):
        url = reverse('user-detail', args=['set_password'])
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.data.get('auth_token'))
        data = {"new_password": "pass1user", "current_password": self.user_data['password']}
        response = self.client.post(url, data=json.dumps(data), content_type='application/json')
        self.assertEqual(status.HTTP_204_NO_CONTENT, response.status_code)

        url = reverse('login')
        login_data = {"username": self.user_data['username'], "password": data['new_password']}
        response = self.client.post(url, data=json.dumps(login_data), content_type='application/json')
        self.assertEqual(status.HTTP_200_OK, response.status_code)

    def test_put_patch(self):
        url = reverse('user-detail', args=['me'])
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.data.get('auth_token'))
        data = {"email": "user1@gmail.com"}
        response = self.client.put(url, data=json.dumps(data), content_type='application/json')
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(data['email'], response.data.get('email'))


class PortfolioTestCase(APITestCase):
    """ тесты API портфеля """
    def setUp(self):
        self.user_1 = User.objects.create(username='test_user1', email='user1@gmail.com', password='testuser123',
                                          first_name='test', last_name='user1')
        self.user_2 = User.objects.create(username='test_user2', email='user2@gmail.com', password='testuser321',
                                          first_name='test', last_name='user2')
        self.portfolio_1 = Portfolio.objects.create(name='test 1', owner=self.user_1)
        self.portfolio_2 = Portfolio.objects.create(name='test 2', owner=self.user_2)

    def test_get(self):
        url = reverse('portfolio-list')
        response = self.client.get(url)
        serializer = PortfolioListSerializer([self.portfolio_1, self.portfolio_2], many=True)
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(serializer.data, response.data)

        url = reverse('portfolio-detail', args=[self.portfolio_1.id])
        response = self.client.get(url)
        serializer = PortfolioListSerializer(self.portfolio_1)
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(serializer.data, response.data)

    def test_get_filter(self):
        url = reverse('portfolio-list')
        response = self.client.get(url, data={'owner__username': 'test_user2'})
        serializer = PortfolioListSerializer(self.portfolio_2)
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual([serializer.data], response.data)

        response = self.client.get(url, data={'search': 'test 1'})
        serializer = PortfolioListSerializer(self.portfolio_1)
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual([serializer.data], response.data)

        response = self.client.get(url, data={'ordering': '-owner'})
        serializer = PortfolioListSerializer([self.portfolio_2, self.portfolio_1], many=True)
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(serializer.data, response.data)

    def test_post_and_delete(self):
        """ create """
        count = Portfolio.objects.count()
        url = reverse('portfolio-list')
        data = {"name": "test potrfolio", "owner": self.user_1.id}
        response = self.client.post(url, data=json.dumps(data), content_type='application/json')
        serializer = PortfolioSerializer(Portfolio.objects.filter(name=response.data.get('name')).first())
        self.assertEqual(status.HTTP_201_CREATED, response.status_code)
        self.assertEqual(serializer.data, response.data)
        self.assertEqual(3, count + 1)

        """ delete """
        url = reverse('portfolio-detail', args=[response.data.get('id')])
        response = self.client.delete(url)
        self.assertEqual(status.HTTP_204_NO_CONTENT, response.status_code)
        self.assertEqual(2, count)

    def test_put_patch(self):
        url = reverse('portfolio-detail', args=[self.portfolio_2.id])
        data = {"name": "portfolio 2", "owner": self.user_1.id}
        response = self.client.put(url, data=json.dumps(data), content_type='application/json')
        expected_data = {"id": self.portfolio_2.id, "name": "portfolio 2", "owner": self.user_1.id}
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(expected_data, response.data)

        url = reverse('portfolio-detail', args=[self.portfolio_2.id])
        data = {"name": "nullable portfolio"}
        response = self.client.patch(url, data=json.dumps(data), content_type='application/json')
        expected_data = {"id": self.portfolio_2.id, "name": "nullable portfolio", "owner": self.user_1.id}
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(expected_data, response.data)


class CompanyTestCase(APITestCase):
    """ тесты API сведений о компаниях(фирмах, организациях) """
    def setUp(self):
        self.industry_1 = Industry.objects.create(name='industry1', description='industry description 1')
        self.industry_2 = Industry.objects.create(name='ind2', description='industry description 2')
        self.country_1 = Country.objects.create(short_name='country1', full_name='full country 1')
        self.country_2 = Country.objects.create(short_name='country2', full_name='country2')

        self.company_1 = Company.objects.create(short_name='company1', full_name='full company 1',
                                                ticker='ABCD', website='page1@website.com',
                                                industry=self.industry_1, country=self.country_1,
                                                description='page 1 description')
        self.company_2 = Company.objects.create(short_name='company2', full_name='company 2',
                                                ticker='EFGH', website='abcd2@website.com',
                                                industry=self.industry_2, country=self.country_2,
                                                description='company 2 description')
        self.company_3 = Company.objects.create(short_name='test_company3', full_name='company 3 full name',
                                                ticker='IKLM', website='efgh3@website.com',
                                                industry=self.industry_1, country=self.country_2,
                                                description='page 3 description')

    def test_get(self):
        url = reverse('companies-list')
        response = self.client.get(url)
        serializer = CompanyListSerializer([self.company_1, self.company_2, self.company_3], many=True)
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(serializer.data, response.data)

        url = reverse('companies-detail', args=[self.company_2.id])
        response = self.client.get(url)
        serializer = CompanyListSerializer(self.company_2)
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(serializer.data, response.data)

    def test_get_filter(self):
        url = reverse('companies-list')
        response = self.client.get(url, data={'short_name': 'company1'})
        serializer = CompanyListSerializer(self.company_1)
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual([serializer.data], response.data)

        response = self.client.get(url, data={'search': 'efgh'})
        serializer = CompanyListSerializer([self.company_2, self.company_3], many=True)
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(serializer.data, response.data)

        response = self.client.get(url, data={'ordering': 'full_name'})
        serializer = CompanyListSerializer([self.company_2, self.company_3, self.company_1], many=True)
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(serializer.data, response.data)

    def test_post_and_delete(self):
        """ create """
        count = Company.objects.count()
        url = reverse('companies-list')
        data = {"short_name": "test_company",
                "full_name": "test_full_company",
                "ticker": "TEST",
                "website": "http://website.com",
                "industry": self.industry_1.id,
                "country": self.country_1.id,
                "description": "test desc"}
        response = self.client.post(url, data=json.dumps(data), content_type='application/json')
        serializer = CompanySerializer(Company.objects.filter(short_name=response.data.get('short_name')).first())
        self.assertEqual(status.HTTP_201_CREATED, response.status_code)
        self.assertEqual(serializer.data, response.data)
        self.assertEqual(4, count + 1)

        """ delete """
        url = reverse('companies-detail', args=[response.data.get('id')])
        response = self.client.delete(url)
        self.assertEqual(status.HTTP_204_NO_CONTENT, response.status_code)
        self.assertEqual(3, count)

    def test_put_patch(self):
        url = reverse('companies-detail', args=[self.company_3.id])
        data = {"short_name": "test_company",
                "full_name": "test_full_company",
                "ticker": "TEST",
                "website": "http://website.com",
                "description": "test desc"}
        response = self.client.put(url, data=json.dumps(data), content_type='application/json')
        self.company_3.refresh_from_db()
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(self.company_3.id, response.data.get('id'))
        self.assertEqual(self.company_3.short_name, response.data.get('short_name'))

        url = reverse('companies-detail', args=[self.company_1.id])
        data = {"full_name": "test full name"}
        response = self.client.patch(url, data=json.dumps(data), content_type='application/json')
        self.company_1.refresh_from_db()
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(self.company_1.id, response.data.get('id'))
        self.assertEqual(self.company_1.full_name, response.data.get('full_name'))


class FundamentalsTestCase(APITestCase):
    """ тесты API фундаментальных показателей компаний """
    def setUp(self):
        self.industry_1 = Industry.objects.create(name='industry1', description='industry description 1')
        self.country_1 = Country.objects.create(short_name='country1', full_name='full country 1')
        self.measure_1 = Measure.objects.create(short_name='measure1', full_name='measure 1 full name')
        self.currency_1 = Currency.objects.create(short_name='currency1', full_name='currency 1 full name')
        self.company_1 = Company.objects.create(short_name='company1', full_name='full company 1',
                                                ticker='ABCD', website='page1@website.com',
                                                industry=self.industry_1, country=self.country_1,
                                                description='page 1 description')

        self.company_fund_1 = Fundamentals.objects.create(company=self.company_1,
                                                          financial_indicators={"EBITDA": "100", "Прибыль": "10"},
                                                          measure=self.measure_1, currency=self.currency_1,
                                                          report_date='2022-11-25', public_date='2022-11-25',
                                                          is_actual=False)
        self.company_fund_2 = Fundamentals.objects.create(company=self.company_1,
                                                          financial_indicators={"EBITDA": "200", "Прибыль": "20"},
                                                          measure=self.measure_1, currency=self.currency_1,
                                                          report_date='2022-11-25', public_date='2022-11-25',
                                                          is_actual=True)
        self.company_fund_3 = Fundamentals.objects.create(company=self.company_1,
                                                          financial_indicators={"EBITDA": "300", "Прибыль": "30"},
                                                          measure=self.measure_1, currency=self.currency_1,
                                                          report_date='2022-11-24', public_date='2022-11-25',
                                                          is_actual=False)

    def test_get(self):
        url = reverse('fundamentals-list', args=[self.company_1.id])
        response = self.client.get(url)
        serializer = FundamentalsListSerializer([self.company_fund_1, self.company_fund_3, self.company_fund_2],
                                                many=True)
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(serializer.data, response.data)

        url = reverse('fundamentals-detail', args=[self.company_1.id, self.company_fund_2.id])
        response = self.client.get(url)
        serializer = FundamentalsListSerializer(self.company_fund_2)
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(serializer.data, response.data)

    def test_get_filter(self):
        url = reverse('fundamentals-list', args=[self.company_1.id])
        response = self.client.get(url, data={'report_date': '2022-11-24'})
        serializer = FundamentalsListSerializer(self.company_fund_3)
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual([serializer.data], response.data)

        response = self.client.get(url, data={'search': 'True'})
        serializer = FundamentalsListSerializer(self.company_fund_2)
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual([serializer.data], response.data)

        response = self.client.get(url, data={'ordering': '-is_actual'})
        serializer = FundamentalsListSerializer([self.company_fund_2, self.company_fund_1, self.company_fund_3],
                                                many=True)
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(serializer.data, response.data)

    def test_post_and_delete(self):
        """ create """
        count = Fundamentals.objects.count()
        url = reverse('fundamentals-list', args=[self.company_1.id])
        data = {"financial_indicators": {"EBITDA": "400"},
                "measure": self.measure_1.id,
                "currency": self.currency_1.id,
                "report_date": "2022-11-25",
                "public_date": "2022-11-25",
                "is_actual": True,
                "source_site": "http://testsite.ru"}
        response = self.client.post(url, data=json.dumps(data), content_type='application/json')
        serializer = FundamentalsSerializer(Fundamentals.objects
                                            .filter(company=self.company_1.id,
                                                    financial_indicators=response.data.get('financial_indicators'))
                                            .first())
        self.assertEqual(status.HTTP_201_CREATED, response.status_code)
        self.assertEqual(serializer.data, response.data)
        self.assertEqual(4, count + 1)

        """ delete """
        url = reverse('fundamentals-detail', args=[self.company_1.id, response.data.get('id')])
        response = self.client.delete(url)
        self.assertEqual(status.HTTP_204_NO_CONTENT, response.status_code)
        self.assertEqual(3, count)

    def test_put_patch(self):
        url = reverse('fundamentals-detail', args=[self.company_1.id, self.company_fund_1.id])
        data = {"financial_indicators": {"EBITDA": "400"},
                "measure": self.measure_1.id,
                "currency": self.currency_1.id,
                "report_date": "2022-11-24",
                "public_date": "2022-11-24",
                "is_actual": True,
                "source_site": "http://testsite.ru"}
        response = self.client.put(url, data=json.dumps(data), content_type='application/json')
        expected_data = {"id": self.company_fund_1.id,
                         "financial_indicators": {"EBITDA": "400"},
                         "measure": self.measure_1.id,
                         "currency": self.currency_1.id,
                         "report_date": "2022-11-24",
                         "public_date": "2022-11-24",
                         "next_public_date": None,
                         "is_actual": True,
                         "source_site": "http://testsite.ru"}
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(expected_data, response.data)

        url = reverse('fundamentals-detail', args=[self.company_1.id, self.company_fund_3.id])
        data = {"financial_indicators": {"EBITDA": "400"}, "report_date": "2022-11-25"}
        response = self.client.patch(url, data=json.dumps(data), content_type='application/json')
        self.company_fund_3.refresh_from_db()
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(self.company_fund_3.id, response.data.get('id'))
        self.assertEqual(self.company_fund_3.financial_indicators, response.data.get('financial_indicators'))


class StockPriceTestCase(APITestCase):
    """ тесты API цен на акции компаний """
    def setUp(self):
        self.industry_1 = Industry.objects.create(name='industry1', description='industry description 1')
        self.country_1 = Country.objects.create(short_name='country1', full_name='full country 1')
        self.currency_1 = Currency.objects.create(short_name='currency1', full_name='currency 1 full name')
        self.company_1 = Company.objects.create(short_name='company1', full_name='full company 1',
                                                ticker='ABCD', website='page1@website.com',
                                                industry=self.industry_1, country=self.country_1,
                                                description='page 1 description')

        self.stock_price_1 = StockPrice.objects.create(company=self.company_1, price=100.10, currency=self.currency_1,
                                                       date_price='2022-11-23T00:00:00Z', is_actual=False)
        self.stock_price_2 = StockPrice.objects.create(company=self.company_1, price=200.10, currency=self.currency_1,
                                                       date_price='2022-11-24T00:00:00Z', is_actual=False)
        self.stock_price_3 = StockPrice.objects.create(company=self.company_1, price=300.10, currency=self.currency_1,
                                                       date_price='2022-11-25T00:00:00Z', is_actual=True)

    def test_get(self):
        url = reverse('stock_prices-list', args=[self.company_1.id])
        response = self.client.get(url)
        serializer = StockPriceSerializer([self.stock_price_1, self.stock_price_2, self.stock_price_3], many=True)
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(serializer.data, response.data)

        url = reverse('stock_prices-detail', args=[self.company_1.id, self.stock_price_3.id])
        response = self.client.get(url)
        serializer = StockPriceSerializer(self.stock_price_3)
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(serializer.data, response.data)

    def test_get_filter(self):
        url = reverse('stock_prices-list', args=[self.company_1.id])
        response = self.client.get(url, data={'is_actual': 'False'})
        serializer = StockPriceSerializer([self.stock_price_1, self.stock_price_2], many=True)
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(serializer.data, response.data)

        response = self.client.get(url, data={'search': '2022-11-25 00:00'})
        serializer = StockPriceSerializer(self.stock_price_3)
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual([serializer.data], response.data)

        response = self.client.get(url, data={'ordering': '-is_actual'})
        serializer = StockPriceSerializer([self.stock_price_3, self.stock_price_1, self.stock_price_2], many=True)
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(serializer.data, response.data)

    def test_post_and_delete(self):
        """ create """
        count = StockPrice.objects.count()
        url = reverse('stock_prices-list', args=[self.company_1.id])
        data = {"price": 400.01,
                "currency": self.currency_1.id,
                "date_price": "2022-11-25T00:01:01Z",
                "is_actual": True}
        response = self.client.post(url, data=json.dumps(data), content_type='application/json')
        serializer = StockPriceSerializer(StockPrice.objects.filter(company=self.company_1.id,
                                                                    date_price=response.data.get('date_price')).first())
        self.assertEqual(status.HTTP_201_CREATED, response.status_code)
        self.assertEqual(serializer.data, response.data)
        self.assertEqual(4, count + 1)

        """ delete """
        url = reverse('stock_prices-detail', args=[self.company_1.id, response.data.get('id')])
        response = self.client.delete(url)
        self.assertEqual(status.HTTP_204_NO_CONTENT, response.status_code)
        self.assertEqual(3, count)

    def test_put_patch(self):
        url = reverse('stock_prices-detail', args=[self.company_1.id, self.stock_price_2.id])
        data = {"price": 400.01,
                "currency": self.currency_1.id,
                "date_price": "2022-11-22T00:01:01Z",
                "is_actual": True}
        response = self.client.put(url, data=json.dumps(data), content_type='application/json')
        expected_data = {"id": self.stock_price_2.id,
                         "price": 400.01,
                         "currency": self.currency_1.id,
                         "date_price": "2022-11-22T00:01:01Z",
                         "is_actual": True}
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(expected_data, response.data)

        url = reverse('stock_prices-detail', args=[self.company_1.id, self.stock_price_1.id])
        data = {"price": 400.01, "date_price": "2022-11-23T00:01:01Z"}
        response = self.client.patch(url, data=json.dumps(data), content_type='application/json')
        self.stock_price_1.refresh_from_db()
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(self.stock_price_1.price, response.data.get('price'))
        self.assertEqual(strftime(self.stock_price_1.date_price, '%Y-%m-%dT%H:%M:%SZ'), response.data.get('date_price'))


class StocksInPortfolioTestCase(APITestCase):
    """ тесты API акций в портфеле """
    def setUp(self):
        self.user_1 = User.objects.create(username='test_user1', email='user1@gmail.com', password='testuser123',
                                          first_name='test', last_name='user1')
        self.user_2 = User.objects.create(username='test_user2', email='user2@gmail.com', password='testuser321',
                                          first_name='test', last_name='user2')
        self.portfolio_1 = Portfolio.objects.create(name='test 1', owner=self.user_1)
        self.portfolio_2 = Portfolio.objects.create(name='test 2', owner=self.user_2)

        self.industry_1 = Industry.objects.create(name='test_industry1', description='industry description 1')
        self.country_1 = Country.objects.create(short_name='test_country1', full_name='country 1 full name')
        self.currency_1 = Currency.objects.create(short_name='currency1', full_name='currency 1 full name')

        self.company_1 = Company.objects.create(short_name='test_company1', full_name='company 1 full name',
                                                ticker='COMP1', website='company1@website.com',
                                                industry=self.industry_1, country=self.country_1,
                                                description='company 1 description')
        self.company_2 = Company.objects.create(short_name='test_company2', full_name='company 2 full name',
                                                ticker='COMP2', website='company2@website.com',
                                                industry=self.industry_1, country=self.country_1,
                                                description='company 2 description')
        self.company_3 = Company.objects.create(short_name='test_company3', full_name='company 3 full name',
                                                ticker='COMP3', website='company3@website.com',
                                                industry=self.industry_1, country=self.country_1,
                                                description='company 3 description')
        self.company_4 = Company.objects.create(short_name='test_company4', full_name='company 4 full name',
                                                ticker='COMP4', website='company4@website.com',
                                                industry=self.industry_1, country=self.country_1,
                                                description='company 4 description')
        self.company_5 = Company.objects.create(short_name='test_company5', full_name='company 5 full name',
                                                ticker='COMP5', website='company5@website.com',
                                                industry=self.industry_1, country=self.country_1,
                                                description='company 5 description')
        self.stock_in_portfolio_1 = StocksInPortfolio.objects.create(portfolio=self.portfolio_1, company=self.company_1,
                                                                     stocks_count=5, buy_price=40.5,
                                                                     invested_amount=202.5, currency=self.currency_1)
        self.stock_in_portfolio_2 = StocksInPortfolio.objects.create(portfolio=self.portfolio_1, company=self.company_2,
                                                                     stocks_count=2, buy_price=39.95,
                                                                     invested_amount=79.9, currency=self.currency_1)
        self.stock_in_portfolio_3 = StocksInPortfolio.objects.create(portfolio=self.portfolio_2, company=self.company_3,
                                                                     stocks_count=16, buy_price=48.3,
                                                                     invested_amount=772.8, currency=self.currency_1)
        self.stock_in_portfolio_4 = StocksInPortfolio.objects.create(portfolio=self.portfolio_2, company=self.company_4,
                                                                     stocks_count=6, buy_price=476.23,
                                                                     invested_amount=2857.38, currency=self.currency_1)

    def test_get(self):
        url = reverse('stocks_portfolio-list', args=[self.portfolio_1.id])
        response = self.client.get(url)
        serializer = StocksInPortfolioListSerializer([self.stock_in_portfolio_1, self.stock_in_portfolio_2], many=True)
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(serializer.data, response.data)

        url = reverse('stocks_portfolio-detail', args=[self.portfolio_1.id, self.stock_in_portfolio_2.id])
        response = self.client.get(url)
        serializer = StocksInPortfolioListSerializer(self.stock_in_portfolio_2)
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(serializer.data, response.data)

    def test_get_filter(self):
        url = reverse('stocks_portfolio-list', args=[self.portfolio_2.id])
        response = self.client.get(url, data={'company__ticker': 'COMP3'})
        serializer = StocksInPortfolioListSerializer(self.stock_in_portfolio_3)
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual([serializer.data], response.data)

        response = self.client.get(url, data={'search': 'full name'})
        serializer = StocksInPortfolioListSerializer([self.stock_in_portfolio_3, self.stock_in_portfolio_4], many=True)
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(serializer.data, response.data)

        response = self.client.get(url, data={'ordering': '-invested_amount'})
        serializer = StocksInPortfolioListSerializer([self.stock_in_portfolio_4, self.stock_in_portfolio_3], many=True)
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(serializer.data, response.data)

    def test_post_and_delete(self):
        """ create """
        count = StocksInPortfolio.objects.count()
        url = reverse('stocks_portfolio-list', args=[self.portfolio_1.id])
        data = {"company": self.company_5.id,
                "stocks_count": 5,
                "buy_price": 10,
                "invested_amount": 50,
                "currency": self.currency_1.id}
        response = self.client.post(url, data=json.dumps(data), content_type='application/json')
        serializer = StocksInPortfolioSerializer(StocksInPortfolio.objects
                                                 .filter(portfolio=self.portfolio_1.id,
                                                         company=response.data.get('company')).first())
        self.assertEqual(status.HTTP_201_CREATED, response.status_code)
        self.assertEqual(serializer.data, response.data)
        self.assertEqual(5, count + 1)

        """ delete """
        url = reverse('stocks_portfolio-detail', args=[self.portfolio_1.id, response.data.get('id')])
        response = self.client.delete(url)
        self.assertEqual(status.HTTP_204_NO_CONTENT, response.status_code)
        self.assertEqual(4, count)

    def test_put_patch(self):
        url = reverse('stocks_portfolio-detail', args=[self.portfolio_2.id, self.stock_in_portfolio_4.id])
        data = {"company": self.company_5.id,
                "stocks_count": 6,
                "buy_price": 40,
                "invested_amount": 240,
                "currency": self.currency_1.id}
        response = self.client.put(url, data=json.dumps(data), content_type='application/json')
        expected_data = {"id": self.stock_in_portfolio_4.id,
                         "company": self.company_5.id,
                         "stocks_count": 6,
                         "buy_price": 40.0,
                         "invested_amount": 240.0,
                         "currency": self.currency_1.id,
                         "portfolio_id": self.portfolio_2.id}
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(expected_data, response.data)

        url = reverse('stocks_portfolio-detail', args=[self.portfolio_2.id, self.stock_in_portfolio_3.id])
        data = {"stocks_count": 6, "buy_price": 40}
        response = self.client.patch(url, data=json.dumps(data), content_type='application/json')
        expected_data = {"id": self.stock_in_portfolio_3.id,
                         "company": self.company_3.id,
                         "stocks_count": 6,
                         "buy_price": 40.0,
                         "invested_amount": 772.8,
                         "currency": self.currency_1.id,
                         "portfolio_id": self.portfolio_2.id}
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(expected_data, response.data)
