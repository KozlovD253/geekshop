from django.shortcuts import render
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.conf import settings
from django.core.cache import cache

from mainapp.models import ProductCategory, Product


def get_links_menu():
    if settings.LOW_CACHE:
        key = 'links_menu'
        links_menu = cache.get(key)
        if links_menu is None:
            links_menu = ProductCategory.objects.all()
            cache.set(key, links_menu)
        return links_menu
    else:
        return ProductCategory.objects.all()

def index(request):
    context = {
        'title': '- главная',
    }
    return render(request, 'mainapp/index.html', context)

def get_products_orederd_by_price():
   if settings.LOW_CACHE:
       key = 'products_orederd_by_price'
       products = cache.get(key)
       if products is None:
           products = Product.objects.all().order_by('price')
           cache.set(key, products)
       return products
   else:
       return Product.objects.all().order_by('price')


def get_products_in_category_orederd_by_price(category_id):
   if settings.LOW_CACHE:
       key = f'products_in_category_orederd_by_price_{category_id}'
       products = cache.get(key)
       if products is None:
           products = Product.objects.filter(category_id=category_id).order_by('price')
           cache.set(key, products)
       return products
   else:
       return Product.objects.filter(category_id=category_id).order_by('price')


def products(request, category_id=None, page=1):
    if category_id:
        #products = Product.objects.filter(category_id=category_id).order_by('price')
        products = get_products_in_category_orederd_by_price(category_id)
    else:
        #products = Product.objects.all().order_by('price')
        products = get_products_orederd_by_price()

    context = {
        'title': '- товары',
        'products': products,
        'category': ProductCategory.objects.all(),
        #'category': get_links_menu(),
    }
    paginator=Paginator(products, 3)
    try:
        products_paginator = paginator.page(page)
    except PageNotAnInteger:
        products_paginator = paginator.page(1)
    except EmptyPage:
        products_paginator = paginator(paginator.num_pages)

    context.update({'products': products_paginator})

    return render(request, 'mainapp/products.html', context)
