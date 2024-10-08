"""mesaagil URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from apps.core.views import overview, dashboard
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path(route='', view=include('apps.core.urls')),
    path(route='admin/', view=admin.site.urls),
    path(route='accounts/', view=include('django.contrib.auth.urls')),
    path(route='restaurants/', view=include('apps.restaurants.urls')),
]

htmx_urlpatterns = [
    path(route='overview/', view=overview, name='overview'),
    path(route='dashboard/', view=dashboard, name='dashboard'),
]

urlpatterns += htmx_urlpatterns

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
