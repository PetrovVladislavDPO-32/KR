from django.test import TestCase, Client
from django.urls import reverse


class WebViewsTests(TestCase):
    def setUp(self):
        self.client = Client()

    def test_home_page(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Добро пожаловать")

    def test_login_page(self):
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Войти")

    def test_tasks_page_unauthorized(self):
        response = self.client.get(reverse('tasks'))
        self.assertEqual(response.status_code, 302)  # Редирект на логин
