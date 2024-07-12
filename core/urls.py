from django.urls import path

from . import views

urlpatterns = [
    path(route='', view=views.home, name='home'),
    path(route='accounts/login/', view=views.login_view, name='login'),
    path(route='accounts/logout/', view=views.logout_view, name='logout'),
]
