from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from django.contrib.auth import get_user_model

User = get_user_model()


def create_user(username='testuser', password='testpass123', role='admin'):
    u = User.objects.create_user(username=username, password=password)
    u.role = role
    u.save()
    return u


class AuthTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = create_user(username='director', password='secret1234', role='superadmin')

    def test_login_returns_tokens(self):
        res = self.client.post('/api/auth/login/', {
            'username': 'director',
            'password': 'secret1234',
        })
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertIn('access', res.data)
        self.assertIn('refresh', res.data)
        self.assertEqual(res.data['role'], 'superadmin')

    def test_login_wrong_password(self):
        res = self.client.post('/api/auth/login/', {
            'username': 'director',
            'password': 'wrongpassword',
        })
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_me_requires_auth(self):
        res = self.client.get('/api/auth/me/')
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_me_returns_user_info(self):
        self.client.force_authenticate(user=self.user)
        res = self.client.get('/api/auth/me/')
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data['username'], 'director')
        self.assertEqual(res.data['role'], 'superadmin')


class UserManagementTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.superadmin = create_user('super', 'pass1234', 'superadmin')
        self.admin = create_user('plain_admin', 'pass1234', 'admin')

    def test_list_users_requires_superadmin(self):
        self.client.force_authenticate(user=self.admin)
        res = self.client.get('/api/users/')
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_superadmin_can_list_users(self):
        self.client.force_authenticate(user=self.superadmin)
        res = self.client.get('/api/users/')
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(res.data), 2)

    def test_superadmin_can_create_user(self):
        self.client.force_authenticate(user=self.superadmin)
        res = self.client.post('/api/users/', {
            'username': 'newadmin',
            'password': 'newpass123',
            'role': 'admin',
        })
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertTrue(User.objects.filter(username='newadmin').exists())

    def test_superadmin_can_delete_user(self):
        self.client.force_authenticate(user=self.superadmin)
        res = self.client.delete(f'/api/users/{self.admin.id}/')
        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)

    def test_cannot_delete_own_account(self):
        self.client.force_authenticate(user=self.superadmin)
        res = self.client.delete(f'/api/users/{self.superadmin.id}/')
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
