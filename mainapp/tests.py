from django.test import TestCase
from django.test.client import Client
from mainapp.models import Product, ProductCategory
from django.core.management import call_command

class TestMainapp(TestCase):

    def SetUp(self):
        cat = ProductCategory.objects.create(
            name='test',
        )
        Product.objects.create(
            category=cat,
            name='test_product_1',

        )
        Product.objects.create(
            category=cat,
            name='test_product_2',

        )
        Product.objects.create(
            category=cat,
            name='test_product_3',

        )
        self.client = Client()

    def test_mainapp_pages(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

    def test_mainapp_shop(self):
        response = self.client.get('/products/')
        self.assertEqual(response.status_code, 200)

        for cat in ProductCategory.objects.all():
            response = self.client.get(f'/products/{cat.pk}/')
            self.assertEqual(response.status_code, 200)

        for prod in Product.objects.all():
            response = self.client.get(f'/products/{cat.pk}/')
            self.assertEqual(response.status_code, 200)


    def tearDown(self) -> None:
        pass
