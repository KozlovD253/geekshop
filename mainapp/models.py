from django.db import models


class ProductCategory(models.Model):
    class Meta:
        verbose_name = 'Категория товара'
        verbose_name_plural = 'Категории товара'

    name = models.CharField(max_length=50, unique=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=100)
    img = models.ImageField(upload_to='product_images', blank=True)
    description = models.TextField(blank=True)
    short_description = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    quantity = models.PositiveIntegerField(default=0)
    category = models.ForeignKey(ProductCategory, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'

    def __str__(self):
        return f'{self.name} {self.category.name}'
