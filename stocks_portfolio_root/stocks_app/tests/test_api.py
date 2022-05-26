from django.urls import reverse
from rest_framework.test import APITestCase

from stocks_app.models import Company
from stocks_app.serializers import CompanySerializer


class CompaniesApiTestCase(APITestCase):
    def test_get(self):
        company_1 = Company.objects.create(short_name='Test name 1', ticker='ticker 1', website='website 1')
        company_2 = Company.objects.create(short_name='Test name 2', ticker='ticker 2', website='website 2')

        url = reverse('company-list')
        response = self.client.get(url)
        serializer_data = CompanySerializer([company_1, company_2], many=True).data
        self.assertEqual(serializer_data, response.data)


