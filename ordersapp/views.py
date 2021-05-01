from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.db.models.signals import pre_save, pre_delete
from django.dispatch import receiver
from django.forms import inlineformset_factory
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy, reverse
from django.utils.decorators import method_decorator
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView

from basketapp.models import Basket
from ordersapp.forms import OrderItemsForm
from ordersapp.models import Order, OrderItems


class OrderList(ListView):
    model = Order

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)

    @method_decorator(login_required())
    def dispatch(self, *args, **kwargs):
        return super(ListView, self).dispatch(*args, **kwargs)


class OrderCreate(CreateView):
    model = Order
    fields = []
    success_url = reverse_lazy('order:orders')

    def get_context_data(self, **kwargs): #переопределили контекст
        data = super().get_context_data(**kwargs)
        OrderFormSet = inlineformset_factory(Order, OrderItems, form=OrderItemsForm, extra=1)

        if self.request.POST:
            formset = OrderFormSet(self.request.POST)
        else:
            basket_items = Basket.objects.filter(user=self.request.user)
            if basket_items.exists():
                OrderFormSet = inlineformset_factory(Order, OrderItems, form=OrderItemsForm, extra=basket_items.count())
                formset = OrderFormSet()
                for num, form in enumerate(formset.forms):
                    form.initial['product'] = basket_items[num].product
                    form.initial['quantity'] = basket_items[num].quantity
                    form.initial['price'] = basket_items[num].product.price
                    form.initial['product_count'] = basket_items[num].product.quantity
            else:
                formset = OrderFormSet()

        data['orderitems'] = formset

        return data

    def form_valid(self, form): #дополнили валидацию формы
        context = self.get_context_data()
        orderitems = context['orderitems']

        with transaction.atomic():
            form.instance.user = self.request.user
            self.object = form.save()
            if orderitems.is_valid():
                orderitems.instance = self.object
                orderitems.save()
                basket_items = Basket.objects.filter(user=self.request.user)
                if basket_items.exists():
                    basket_items.delete()


        if self.object.get_total_cost() == 0:
            self.object.delete()

        return super().form_valid(form)

    # @method_decorator(login_required())
    # def dispatch(self, *args, **kwargs):
    #     return super(ListView, self).dispatch(*args, **kwargs)

class OrderUpdate(UpdateView):
    model = Order
    fields = []
    success_url = reverse_lazy('order:orders')

    def get_context_data(self, **kwargs):  # переопределили контекст
        data = super().get_context_data(**kwargs)
        OrderFormSet = inlineformset_factory(Order, OrderItems, form=OrderItemsForm, extra=1)

        if self.request.POST:
            formset = OrderFormSet(self.request.POST, instance=self.object)
        else:
            formset = OrderFormSet(instance=self.object)
            for form in formset.forms:
                if form.instance.pk:
                    form.initial['price'] = form.instance.product.price
                    form.initial['product_count'] = form.instance.product.quantity

        data['orderitems'] = formset

        return data

    def form_valid(self, form):  # дополнили валидацию формы
        context = self.get_context_data()
        orderitems = context['orderitems']

        with transaction.atomic():
            self.object = form.save()
            if orderitems.is_valid():
                orderitems.instance = self.object
                orderitems.save()
        if self.object.get_total_cost() == 0:
            self.object.delete()

        return super().form_valid(form)

    # @method_decorator(login_required())
    # def dispatch(self, *args, **kwargs):
    #     return super(ListView, self).dispatch(*args, **kwargs)


class OrderDelete(DeleteView):
    model = Order
    success_url = reverse_lazy('order:orders')


class OrderDetail(DetailView):
    model = Order


def order_forming_complete(request, pk):
    order = get_object_or_404(Order, pk=pk)
    order.status = Order.SENT_TO_PROCEED
    order.save()

    return HttpResponseRedirect(reverse('order:orders'))

@receiver(pre_save, sender=Basket)
@receiver(pre_save, sender=OrderItems)
def product_quantity_update_save(sender, update_fields, instance, **kwargs):   #возврат товаров на склад при удалении корзины или заказа
    if update_fields is 'quantity' or 'product':
        if instance.pk:
            instance.product.quantity -= instance.quantity - sender.get_item(instance.pk).quantity
        else:
            instance.product.quantity -= instance.quantity

        instance.product.save()


@receiver(pre_delete, sender=Basket)
@receiver(pre_delete, sender=OrderItems)
def product_quantity_update_delete(sender, instance, **kwargs):
    instance.product.quantity += instance.quantity
    instance.product.save()