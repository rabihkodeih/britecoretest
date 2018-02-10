'''
Created on Feb 4, 2018

@author: rabihkodeih
'''
from django.urls.conf import path
from django.shortcuts import render



def index(request):
    context = {}
    return render(request, 'index.html', context)


urls = [path('', index, name='url_index'),
        path('index/', index, name='url_index')]
