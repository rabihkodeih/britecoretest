'''
Created on Feb 24, 2018

@author: rabihkodeih
'''
from django.utils.six import wraps
from django.http.response import HttpResponseForbidden


def requires_authentication(view):
    @wraps(view)
    def wrapper(request, *args, **kwargs):
        if request.user.is_authenticated:
            result = view(request, *args, **kwargs)
            return result
        return HttpResponseForbidden()
    return wrapper