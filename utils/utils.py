from django.conf import settings
from django.http import HttpRequest


def build_next_path(request: HttpRequest) -> str:
    '''Builds the next path for the non-logged user'''
    return f"{settings.LOGIN_URL}?next={request.path}"


def get_next_path(request: HttpRequest) -> str:
    '''Gets the next path to redirect the user'''
    try:
        return request.GET['next']
    except:
        return 'home'


def get_remeber(request: HttpRequest) -> str | None:
    '''
    Gets the remember value if it exists 
    otherwise return None
    '''
    try:
        return request.POST['remember']
    except:
        return None
