import logging

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

from utils.utils import build_next_path, get_next_path, get_remeber
from apps.restaurants.models import Products

logger = logging.getLogger(__name__)


def login_view(request):
    COOKIE_AGE = (604800 * 3)  # 3 weeks in seconds

    if request.method == 'POST':
        next_path = get_next_path(request=request)
        email = request.POST['email']
        password = request.POST['password']
        remember = get_remeber(request=request)

        if not email or not password:
            messages.add_message(
                request=request, 
                level=messages.ERROR, 
                message='Você precisa preencher Email e Senha válidos para entrar.'
            )
            return render(
                request=request, 
                template_name='registration/login.html'
            )

        user = authenticate(
            request=request, 
            email=email, 
            password=password
        )

        if user is None:
            messages.add_message(
                request=request, 
                level=messages.WARNING, 
                message='Email ou Senha icorreto!\
                     Não foi possível encontrar o usuário.\
                     Tente novamente.'
            )
            return render(
                request=request, 
                template_name='registration/login.html'
            )

        login(request, user)

        if remember:
            request.session.set_expiry(COOKIE_AGE)
        else:
            request.session.set_expiry(0)
            request.session.modified = True

        request.session.save()
        return redirect(next_path)

    return render(
        request=request, 
        template_name='registration/login.html'
    )


def logout_view(request):
    messages.add_message(
        request=request, 
        level=messages.SUCCESS, 
        message='Você saiu do Mesaagil, volte sempre!'
    )
    logout(request)

    return redirect('login')


def home(request):
    if not request.user.is_authenticated:
        return redirect(build_next_path(request))

    context = {}
    products = Products.objects.all()
    context = {'products': products}

    return render(
        request=request,
        template_name='base.html',
        context=context
    )


def overview(request):
    if not request.user.is_authenticated:
        return redirect(build_next_path(request))

    return render(
        request=request, 
        template_name='overview.html'
    )


def dashboard(request):
    if not request.user.is_authenticated:
        return redirect(build_next_path(request))

    return render(
        request=request, 
        template_name='dashboard.html'
    )
