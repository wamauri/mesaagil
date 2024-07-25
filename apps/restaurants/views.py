import io, base64

from django.shortcuts import render, redirect
from django.contrib.auth.models import Group
from django.contrib import messages
from taggit.models import Tag, TaggedItem

from utils.utils import build_next_path
from utils.images import compress_image
from .forms import WaiterForm, ProductsForm, FoodImageForm
from .models import FoodImage


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

    context = {}

    if request.method == 'POST':
        pform = ProductsForm(request.POST or None)
        iform = FoodImageForm(request.POST, request.FILES)
        image = request.POST.get('image_data')
        tags = [tag.upper() for tag in request.POST.get('tags').split(',')]

        if pform.is_valid() and iform.is_valid() and image:

            compressed_image = compress_image(image)
            food_image = FoodImage()
            food_image.image.save(compressed_image.name, compressed_image)
            food_image.save()

            product = pform.save()
            for tag in tags:
                product.category.add(tag)
            product.food_image = food_image
            product.user = request.user
            product.save()
            context['pform'] = ProductsForm()
            context['iform'] = FoodImageForm()
            
            messages.add_message(
                request=request, 
                level=messages.SUCCESS, 
                message=f'{product.name} criado com sucesso!'
            )

            return render(
                request=request, 
                template_name='create_products.html', 
                context=context
            )

        messages.add_message(
            request=request, 
            level=messages.ERROR, 
            message='Algo deu errado ao criar produto!'
        )
    else:
        pform = ProductsForm()
        iform = FoodImageForm()

    context = {
        'pform': pform,
        'iform': iform,
    }

    return render(
        request=request, 
        template_name='create_products.html',
        context=context
    )


def get_product_categories(request):
    if not request.user.is_authenticated:
        return redirect(build_next_path(request))
    return Tag.objects.all()


def get_products_tagged(request):
    if not request.user.is_authenticated:
        return redirect(build_next_path(request))
    # Products.objects.filter(category__name__in=['T1'])
    return TaggedItem.objects.all()
