from django.contrib.auth.models import User
from stocks_app.serializers import PortfolioListSerializer, PortfolioSerializer
import json
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from stocks_app.models import Company, Portfolio


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

    def test_create(self):
        self.assertEqual(status.HTTP_201_CREATED, self.user.status_code)
        self.assertEqual(status.HTTP_200_OK, self.token.status_code)
        print(self.token.data)

    def test_get(self):
        url = reverse('user-detail', args=['me'])
        response = self.client.get(url)
        self.assertEqual(status.HTTP_401_UNAUTHORIZED, response.status_code)
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

    def test_delete(self):
        url = reverse('user-detail', args=['me'])
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.data.get('auth_token'))
        data = {"current_password": self.user_data['password']}
        response = self.client.delete(url, data=json.dumps(data), content_type='application/json')
        self.assertEqual(status.HTTP_204_NO_CONTENT, response.status_code)

        url = reverse('login')
        login_data = {"username": self.user_data['username'], "password": self.user_data['password']}
        response = self.client.post(url, data=json.dumps(login_data), content_type='application/json')
        self.assertEqual(status.HTTP_401_UNAUTHORIZED, response.status_code)

    def test_token_destroy(self):
        url = reverse('logout')
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.data.get('auth_token'))
        response = self.client.post(url)
        self.assertEqual(status.HTTP_204_NO_CONTENT, response.status_code)

        url = reverse('user-detail', args=['me'])
        response = self.client.get(url)
        self.assertEqual(status.HTTP_401_UNAUTHORIZED, response.status_code)


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

    def test_post(self):
        count = Portfolio.objects.count()
        url = reverse('portfolio-list')
        data = {"name": "test potrfolio", "owner": self.user_1.id}
        response = self.client.post(url, data=json.dumps(data), content_type='application/json')
        serializer = PortfolioSerializer(Portfolio.objects.filter(name=response.data.get('name')).first())
        self.assertEqual(status.HTTP_201_CREATED, response.status_code)
        self.assertEqual(serializer.data, response.data)
        self.assertEqual(3, count + 1)

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

    def test_delete(self):
        count = Portfolio.objects.count()
        url = reverse('portfolio-detail', args=[self.portfolio_1.id])
        response = self.client.delete(url)
        self.assertEqual(status.HTTP_204_NO_CONTENT, response.status_code)
        self.assertEqual(1, count - 1)
