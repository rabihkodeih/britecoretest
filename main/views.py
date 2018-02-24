'''
Created on Feb 4, 2018

@author: rabihkodeih
'''
from django.urls.conf import path
from django.shortcuts import render
from django.contrib.auth.decorators import login_required


@login_required
def home(request):
    context = {}
    return render(request, 'home.html', context)


urls = [path('', home, name='url_home'),
        path('home/', home, name='url_home')]
