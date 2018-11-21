"""britecore URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
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
from django.conf.urls import url
from django.contrib.auth import views as auth_views

from main import views
from main import api
from britecore.settings import LOGIN_URL

urlpatterns = [
    # admin views
    path(r'admin/', admin.site.urls),
    # login view
    path(LOGIN_URL[1:], auth_views.LoginView.as_view(), name='url_login'),
    # logout view
    path(r'logout/', auth_views.LogoutView.as_view(), name='url_logout'),
    # web views
    url(r'', include(views.urls)),
    # api views
    url(r'api/', include(api.urls)),
]


# end of file
