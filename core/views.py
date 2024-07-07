from django.shortcuts import render


def home(request):
    return render(
        request=request,
        template_name='base.html'
    )


def overview(request):
    return render(request, 'overview.html')


def dashboard(request):
    return render(request, 'dashboard.html')
