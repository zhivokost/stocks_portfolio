import json

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from stocks_app.models import Company
from stocks_app.serializers import CompanySerializer


class CompaniesApiTestCase(APITestCase):
    def setUp(self):
        self.company_1 = Company.objects.create(short_name='Test name 1',
                                                ticker='ticker 1',
                                                website='website 1')
        self.company_2 = Company.objects.create(short_name='Test name 2',
                                                ticker='ticker 2',
                                                website='website 2')
        self.company_3 = Company.objects.create(short_name='Test name ticker 1',
                                                ticker='ticker 2',
                                                website='website 2')

    def test_get(self):
        url = reverse('company-list')
        response = self.client.get(url)
        print(response.data)
        serializer_data = CompanySerializer([self.company_1, self.company_2, self.company_3], many=True).data
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(serializer_data, response.data)

    def test_get_filter(self):
        url = reverse('company-list')
        response = self.client.get(url, data={'ticker': 'ticker 2'})
        print(response.data)
        serializer_data = CompanySerializer([self.company_2, self.company_3], many=True).data
        print(serializer_data)
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(serializer_data, response.data)

    def test_get_search(self):
        url = reverse('company-list')
        response = self.client.get(url, data={'search': 'ticker 1'})
        print(response.data)
        serializer_data = CompanySerializer([self.company_1, self.company_3], many=True).data
        print(serializer_data)
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(serializer_data, response.data)

    def test_create(self):
        count = Company.objects.all().count()
        url = reverse('company-list')
        data = {
            "short_name": "ЛУКОЙЛ",
            "ticker": "LKOH",
            "website": "http://lukoil.ru"
        }
        json_data = json.dumps(data)
        response = self.client.post(url, data=json_data,
                                   content_type='application/json')

        self.assertEqual(status.HTTP_201_CREATED, response.status_code)
        self.assertEqual(count + 1, Company.objects.all().count())
