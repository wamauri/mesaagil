from django.conf import settings


def redirect_user(request):
    return f"{settings.LOGIN_URL}?next={request.path}"
