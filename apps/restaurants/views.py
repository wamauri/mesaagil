from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import Group
from django.contrib import messages

from utils.utils import build_next_path
from utils.images import product_image_name, prepare_images
from .forms import (
    WaiterForm, ProductsForm, 
    FoodImageForm, CategoryForm, 
    SelectCategoryForm
)
from .models import Category, Products


def create_waiter(request):
    if not request.user.is_authenticated:
        return redirect(build_next_path(request))

    context = {}
    form = WaiterForm(request.POST or None)

    if request.method == 'POST':
        waiter_group = Group.objects.get(name='Waiter')

        if form.is_valid():
            password = form.cleaned_data['password']
            waiter = form.save()
            waiter.set_password(password)
            waiter.groups.add(waiter_group)
            waiter.is_waiter = True
            waiter.save()
            context['form'] = WaiterForm()
            messages.add_message(
                request=request, 
                level=messages.SUCCESS, 
                message='Garçon criado com sucesso!'
            )

            return render(
                request=request, 
                template_name='create_waiter.html', 
                context=context
            )
        messages.add_message(
            request=request, 
            level=messages.ERROR, 
            message='Algo deu errado ao criar Garçon!'
        )
    else:
        form = WaiterForm()

    context = {'form': form}

    return render(
        request=request, 
        template_name='create_waiter.html', 
        context=context
    )


def create_products(request):
    if not request.user.is_authenticated:
        return redirect(build_next_path(request))

    if request.method == 'POST':
        form = ProductsForm(request.POST)

        if form.is_valid():
            product = form.save(commit=False)
            product.user = request.user
            product.save()

            return render(
                request=request, 
                template_name='partials/upload_product_image.html', 
                context={'product': product, 'form': FoodImageForm()}
            )
    else:
        form = ProductsForm()

    return render(
        request=request, 
        template_name='create_products.html', 
        context={'form': form}
    )


def upload_product_image(request, product_id):
    if not request.user.is_authenticated:
        return redirect(build_next_path(request))

    product = get_object_or_404(Products, id=product_id)

    if request.method == 'POST':
        form = FoodImageForm(request.POST, request.FILES, instance=product)
        image = request.POST.get('image_data')

        if product:
            file_name = product_image_name(product)

        if form.is_valid() and image:
            product.food_image = prepare_images(image, file_name)
            product.save()
            context = {
                'categories': Category.objects.all(),
                'form': CategoryForm(),
                'form_select': SelectCategoryForm(),
                'product': product
            }

            return render(
                request=request, 
                template_name='category.html', 
                context=context
            )
    else:
        form = FoodImageForm(instance=product)
    return render(
        request=request, 
        template_name='partials/upload_product_image.html', 
        context={'form': form, 'product': product}
    )


def add_product_category(request, product_id: int):
    if not request.user.is_authenticated:
        return redirect(build_next_path(request))

    if request.method == "POST":
        product = get_object_or_404(Products, id=product_id)
        try:
            category_id = int(request.POST.get('parent'))
            category = get_object_or_404(Category, id=category_id)
            product.category = category
            product.save()

            if request.POST['action'] == 'another':
                return redirect('products-new')
            return redirect('/')
        except:
            context = {
                'product': product,
                'form': CategoryForm(),
                'form_select': SelectCategoryForm()
            }
            messages.add_message(
                request=request, 
                level=messages.ERROR, 
                message=f'Category not selected'
            )
            return render(request, 'category.html', context)
    return render(request, 'category.html')


def add_category(request, product_id: int):
    if not request.user.is_authenticated:
        return redirect(build_next_path(request))

    product = get_object_or_404(Products, id=product_id)

    if request.method == 'POST':
        form = CategoryForm(request.POST)

        if form.is_valid():
            form.save()

            context = {
                'categories': Category.objects.all(),
                'form': CategoryForm(),
                'form_select': SelectCategoryForm(),
                'product': product
            }

            return render(
                request=request, 
                template_name='category.html', 
                context=context
            )

    else:
        form = CategoryForm()
        context = {
            'form': form,
            'product': product
        }

    return render(
        request=request, 
        template_name='partials/modal_add_category.html', 
        context=context
    )


def product_detail(request, product_id):
    if not request.user.is_authenticated:
        return redirect(build_next_path(request))

    return render(
        request=request, 
        template_name='partials/modal_product_detail.html', 
        context={'product_detail': get_object_or_404(Products, id=product_id)}
    )


def filter_products_by_category(request):
    context = {}
    products = None
    if not request.user.is_authenticated:
        return redirect(build_next_path(request))

    if request.method == 'POST':
        category_name = request.POST.get('category')
        category = Category.objects.filter(name=category_name)

        if category:
           products = category[0].products.all()

        context['products'] =  products

        return render(
            request=request, 
            template_name='partials/cards.html', 
            context=context
        )


def lobby(request):
    return render(request, 'chat/lobby.html')
