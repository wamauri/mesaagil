from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from utils.utils import redirect_user


def login_view(request):

    if request.method == 'POST':
        try:
            next_path = request.GET['next']
        except:
            next_path = 'home'
        email = request.POST["email"]
        password = request.POST["password"]
        user = authenticate(request=request, email=email, password=password)

        if user is not None:
            login(request, user)
            if next_path:
                return redirect(next_path)
            else:
                return redirect('home')
        else:
            return redirect(request.path)

    return render(request, template_name="registration/login.html")


def logout_view(request):
    logout(request)
    return redirect('login')


def home(request):
    if not request.user.is_authenticated:
        return redirect(redirect_user(request))

    return render(
        request=request,
        template_name='base.html'
    )


def overview(request):
    if not request.user.is_authenticated:
        return redirect(redirect_user(request))
    return render(request, 'overview.html')


def dashboard(request):
    if not request.user.is_authenticated:
        return redirect(redirect_user(request))
    return render(request, 'dashboard.html')
