from django.db import connection
from django.db.models import F
from django.shortcuts import render, HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.contrib.auth.decorators import user_passes_test
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.utils.decorators import method_decorator
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from authapp.models import User
from mainapp.models import Product, ProductCategory
from adminapp.forms import UserAdminRegisterForm, UserAdminProfileForm, UserAdminCreateProductForm, \
    UserAdminCreateCategoryForm


@user_passes_test(lambda user: user.is_superuser)
def index(request):
    return render(request, 'adminapp/index.html')


class UsersListView(ListView):
    model = User
    template_name = 'adminapp/admin-users-read.html'
    paginate_by = 3

    @method_decorator(user_passes_test(lambda user: user.is_superuser))
    def dispatch(self, request, *args, **kwargs):
        return super(UsersListView, self).dispatch(request, *args, **kwargs)


# @user_passes_test(lambda user: user.is_superuser)
# def admin_users(request):
#     context = {
#         'users': User.objects.all(),
#     }
#     return render(request, 'adminapp/admin-users-read.html', context)


class UserCreateView(CreateView):
    model = User
    template_name = 'adminapp/admin-users-create.html'
    success_url = reverse_lazy('admin_staff:admin_users')
    form_class = UserAdminRegisterForm

    @method_decorator(user_passes_test(lambda user: user.is_superuser))
    def dispatch(self, request, *args, **kwargs):
        return super(UserCreateView, self).dispatch(request, *args, **kwargs)


# @user_passes_test(lambda user: user.is_superuser)
# @user_passes_test(lambda user: user.is_superuser)
# def admin_users_create(request):
#     if request.method == 'POST':
#         form = UserAdminRegisterForm(data=request.POST, files=request.FILES)
#         if form.is_valid():
#             form.save()
#             return HttpResponseRedirect(reverse('admin_staff:admin_users'))
#     else:
#         form = UserAdminRegisterForm()
#
#     context = {'form': form}
#
#     return render(request, 'adminapp/admin-users-create.html', context)


class UserUpdateView(UpdateView):
    model = User
    template_name = 'adminapp/admin-users-update-delete.html'
    success_url = reverse_lazy('admin_staff:admin_users')
    form_class = UserAdminProfileForm

    def get_context_data(self, **kwargs):  # добавление контекста
        context = super(UserUpdateView, self).get_context_data(**kwargs)
        context.update({'title': 'Geekshop - редактирование пользователя'})
        return context

    @method_decorator(user_passes_test(lambda user: user.is_superuser))
    def dispatch(self, request, *args, **kwargs):
        return super(UserUpdateView, self).dispatch(request, *args, **kwargs)


# @user_passes_test(lambda user: user.is_superuser)
# def admin_users_update(request, user_id):
#     user = User.objects.get(id=user_id)
#     if request.method == 'POST':
#         form = UserAdminProfileForm(data=request.POST, files=request.FILES, instance=user)
#         if form.is_valid():
#             form.save()
#             return HttpResponseRedirect(reverse('admin_staff:admin_users'))
#     else:
#         form = UserAdminProfileForm(instance=user)
#
#     context = {'form': form, 'user': user}
#     return render(request, 'adminapp/admin-users-update-delete.html', context)


class UserDeleteView(DeleteView):
    model = User
    template_name = 'adminapp/admin-users-update-delete.html'
    success_url = reverse_lazy('admin_staff:admin_users')

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.is_active = False
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())


# @user_passes_test(lambda user: user.is_superuser)
# def admin_users_remove(request, user_id):
#     user = User.objects.get(id=user_id)
#     user.is_active = False
#     user.save()
#     return HttpResponseRedirect(reverse('admin_staff:admin_users'))


class ProductsListView(ListView):
    model = Product
    template_name = 'adminapp/admin-product-read.html'
    paginate_by = 2

    @method_decorator(user_passes_test(lambda user: user.is_superuser))
    def dispatch(self, request, *args, **kwargs):
        return super(ProductsListView, self).dispatch(request, *args, **kwargs)
# @user_passes_test(lambda user: user.is_superuser)
# def admin_products(request):
#     context = {
#         'products': Product.objects.all(),
#     }
#     return render(request, 'adminapp/admin-product-read.html', context)

class ProductCreateView(CreateView):
    model = Product
    template_name = 'adminapp/admin-product-create.html'
    success_url = reverse_lazy('admin_staff:admin_products')
    form_class = UserAdminCreateProductForm

    @method_decorator(user_passes_test(lambda user: user.is_superuser))
    def dispatch(self, request, *args, **kwargs):
        return super(ProductCreateView, self).dispatch(request, *args, **kwargs)
# @user_passes_test(lambda user: user.is_superuser)
# def admin_products_create(request):
#     if request.method == 'POST':
#         form = UserAdminCreateProductForm(data=request.POST, files=request.FILES)
#         if form.is_valid():
#             form.save()
#             return HttpResponseRedirect(reverse('admin_staff:admin_products'))
#     else:
#         form = UserAdminCreateProductForm()
#
#     context = {'form': form}
#
#     return render(request, 'adminapp/admin-product-create.html', context)


class ProductUpdateView(UpdateView):
    model = Product
    template_name = 'adminapp/admin-products-update-delete.html'
    success_url = reverse_lazy('admin_staff:admin_products')
    form_class = UserAdminCreateProductForm

    @method_decorator(user_passes_test(lambda user: user.is_superuser))
    def dispatch(self, request, *args, **kwargs):
        return super(ProductUpdateView, self).dispatch(request, *args, **kwargs)
# @user_passes_test(lambda user: user.is_superuser)
# def admin_products_update(request, product_id):
#     product = Product.objects.get(id=product_id)
#     if request.method == 'POST':
#         form = UserAdminCreateProductForm(data=request.POST, files=request.FILES, instance=product)
#         if form.is_valid():
#             form.save()
#             return HttpResponseRedirect(reverse('admin_staff:admin_products'))
#     else:
#         form = UserAdminCreateProductForm(instance=product)
#
#     context = {'form': form, 'product': product}
#     return render(request, 'adminapp/admin-products-update-delete.html', context)


class ProductDeleteView(DeleteView):
    model = Product
    success_url = reverse_lazy('admin_staff:admin_products')

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.delete()
        return HttpResponseRedirect(self.get_success_url())
# @user_passes_test(lambda user: user.is_superuser)
# def admin_products_remove(request, product_id):
#     product = Product.objects.get(id=product_id)
#     product.delete()
#     return HttpResponseRedirect(reverse('admin_staff:admin_products'))

class CategoryListView(ListView):
    model = ProductCategory
    template_name = 'adminapp/admin-category-read.html'
    paginate_by = 2

    @method_decorator(user_passes_test(lambda user: user.is_superuser))
    def dispatch(self, request, *args, **kwargs):
        return super(CategoryListView, self).dispatch(request, *args, **kwargs)

class CategoryUpdateView(UpdateView):
    model = ProductCategory
    template_name = 'adminapp/admin-category-update-delete.html'
    success_url = reverse_lazy('admin_staff:admin_category')
    form_class = UserAdminCreateCategoryForm

    @method_decorator(user_passes_test(lambda user: user.is_superuser))
    def dispatch(self, request, *args, **kwargs):
        return super(CategoryUpdateView, self).dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        if 'discount' in form.cleaned_data:
            discount = form.cleaned_data['discount']
            if discount:
                print()
                self.object.product_set.update(price=F('price') * (1 - discount / 100))
        return super().form_valid(form)

class CategoryDeleteView(DeleteView):
    model = ProductCategory
    success_url = reverse_lazy('admin_staff:admin_category')

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.delete()
        return HttpResponseRedirect(self.get_success_url())

class CategoryCreateView(CreateView):
    model = ProductCategory
    template_name = 'adminapp/admin-category-create.html'
    success_url = reverse_lazy('admin_staff:admin_category')
    form_class = UserAdminCreateCategoryForm

    @method_decorator(user_passes_test(lambda user: user.is_superuser))
    def dispatch(self, request, *args, **kwargs):
        return super(CategoryCreateView, self).dispatch(request, *args, **kwargs)