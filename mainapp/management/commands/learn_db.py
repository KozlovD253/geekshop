from django.core.management import BaseCommand
from mainapp.models import Product, ProductCategory
from django.db import connection
from django.db.models import Q
from django.db.models import F, When, Case, DecimalField, IntegerField
from datetime import timedelta

from ordersapp.models import OrderItems


def db_profile_by_type(prefix, type, queries):
   update_queries = list(filter(lambda x: type in x['sql'], queries))
   print(f'db_profile {type} for {prefix}:')
   [print(query['sql']) for query in update_queries]

class Command(BaseCommand):

    def handle(self, *args, **options):
        # test_products = Product.objects.filter(
        #     Q(category__name='Одежда') |
        #     Q(category__name='Аксессуары')
        # )
        #
        # #print(len(test_products))
        # print(test_products.select_related())
        #
        # db_profile_by_type('learn db', '', connection.queries)

        ACTION_1 = 1
        ACTION_2 = 2
        ACTION_EXPIRED = 3

        action_1__time_delta = timedelta(hours=12)
        action_2__time_delta = timedelta(days=1)

        action_1__discount = 0.3
        action_2__discount = 0.15
        action_expired__discount = 0.05

        action_1__condition = Q(order__updated_at__lte=F('order__created_at') + \
                                                    action_1__time_delta)

        action_2__condition = Q(order__updated_at__gt=F('order__created_at') + \
                                                   action_1__time_delta) & \
                              Q(order__updated_at__lte=F('order__created_at') + \
                                                    action_2__time_delta)

        action_expired__condition = Q(order__updated_at__gt=F('order__created_at') + \
                                                         action_2__time_delta)

        action_1__order = When(action_1__condition, then=ACTION_1)
        action_2__order = When(action_2__condition, then=ACTION_2)
        action_expired__order = When(action_expired__condition, then=ACTION_EXPIRED)

        action_1__price = When(action_1__condition,
                               then=F('product__price') * F('quantity') * action_1__discount)

        action_2__price = When(action_2__condition,
                               then=F('product__price') * F('quantity') * -action_2__discount)

        action_expired__price = When(action_expired__condition,
                                     then=F('product__price') * F('quantity') * action_expired__discount)

        test_orders = OrderItems.objects.annotate(
            action_order=Case(
                action_1__order,
                action_2__order,
                action_expired__order,
                output_field=IntegerField(),
            )).annotate(
            total_price=Case(
                action_1__price,
                action_2__price,
                action_expired__price,
                output_field=DecimalField(),
            )).order_by('action_order', 'total_price').select_related()

        for orderitem in test_orders:
            print(f'{orderitem.action_order:2}: заказ №{orderitem.pk:3}:\
                   {orderitem.product.name:15}: скидка\
                   {abs(orderitem.total_price):6.2f} руб. | \
                   {orderitem.order.updated_at - orderitem.order.created_at}')