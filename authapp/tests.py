from django.conf import settings
from django.test import TestCase, Client

from authapp.models import User


class TestUserAuthTestCase(TestCase):
    username = 'django'
    email = 'dj@gb.local'
    password = 'Geek0000'

    def setUp(self):
        self.admin = User.objects.create_superuser(self.username, self.email, self.password)
        self.client = Client()

    def test_user_login(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context['user'].is_anonymous)
        self.assertNotContains(response, 'Выйти')

        self.client.login(username=self.username, password=self.password)

        response = self.client.get('/auth/login/')
        self.assertFalse(response.context['user'].is_anonymous)
        self.assertEqual(response.context['user'], self.admin)

        response = self.client.get('/')
        self.assertFalse(response.context['user'].is_anonymous)
        self.assertContains(response, 'Выйти')

    def test_basket_login_redirect(self):
        response = self.client.get('/auth/profile/')
        self.assertEqual(response.url, '/auth/login/?next=/auth/profile/')
        self.assertEqual(response.status_code, 302)

        self.client.login(username=self.username, password=self.password)

        response = self.client.get('/auth/profile/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(list(response.context['baskets']), [])

    def test_user_register(self):
        response = self.client.get('/auth/register/')
        self.assertEqual(response.status_code, 200)

        new_user_data = {
            'username': 'django2',
            'email': 'email@email.local',
            'password1': self.password,
            'password2': self.password,
            'first_name': 'Fartrew',
            'last_name': 'Fartrew',

        }

        response = self.client.post('/auth/register/', data=new_user_data)
        self.assertEqual(response.status_code, 302)

        new_user = User.objects.get(username='django2')

        activation_url = f'{settings.DOMAIN}/auth/verify/{new_user_data["email"]}/{new_user.activation_key}'
        self.client.get(activation_url)

        self.client.login(username=new_user_data['username'], password=new_user_data['password1'])
        response = self.client.get('/auth/profile/')

        self.assertEqual(response.status_code, 200)
