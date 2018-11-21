from django.urls.conf import path
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from britecore.settings import LOGIN_URL


@login_required(login_url=LOGIN_URL)
def home(request):
    context = {}
    return render(request, 'home.html', context)


urls = [path('', home, name='url_default'),
        path('home/', home, name='url_home')]


# end of file
