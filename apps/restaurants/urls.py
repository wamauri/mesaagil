from django.urls import path

from . import views

urlpatterns = [
    path(route='new/', view=views.create_waiter, name='new' )
]
