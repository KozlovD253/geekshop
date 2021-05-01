from django.db import models
from authapp.models import User

from mainapp.models import Product
from django.utils.functional import cached_property


#ОБРАБОТКА УДАЛЕНИЯ КОРЗИНЫ ВАРИАНТ 1
# #менеджер модели. класс для обработи событий, происходящих с querySet
# class BasketQuerySet(models.QuerySet):
#
#     def delete(self):
#         for obj in self:
#             obj.product.quantity += obj.quantity
#             obj.product.save()
#
#         super().delete()


class Basket(models.Model):
    # objects = BasketQuerySet.as_manager() #привязываем менеджер модели к модели

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='basket')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveSmallIntegerField(default=0)
    created_timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Корзина'
        verbose_name_plural = 'Корзины'

    def __str__(self):
        return f'Корзина для пользователя {self.user.username}, товар {self.product.name}'

    @cached_property
    def get_items_cached(self):
        return self.user.basket.select_related()

    def sum(self):
        return self.quantity * self.product.price

    def total_quantity(self):
        #baskets = Basket.objects.filter(user=self.user)
        baskets = self.get_items_cached
        return sum(basket.quantity for basket in baskets)

    def total_sum(self):
        # baskets = Basket.objects.filter(user=self.user)
        baskets = self.get_items_cached
        return sum(basket.sum() for basket in baskets)

    @staticmethod
    def get_item(pk):
        return Basket.objects.filter(pk=pk).first()

    # ОБРАБОТКА УДАЛЕНИЯ ТОВАРА ИЗ КОРЗИНЫ ВАРИАНТ 1
    # def delete(self): #переопределяем, чтобы вернуть товар на склад при удалении из корзины
    #     self.product.quantity += self.quantity
    #     self.product.save()
    #     super().delete()
