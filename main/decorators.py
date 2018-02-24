'''
Created on Feb 24, 2018

@author: rabihkodeih
'''
from django.utils.six import wraps
from django.http.response import HttpResponseForbidden


def requires_authentication(view):
    '''
    This decorator is used to decorate api views in order to make sure
    that only authenticated users can use the api. Unauthorized of anonymous
    users will receive an HTTP 403 FORBIDDEN response.
    '''
    @wraps(view)
    def wrapper(request, *args, **kwargs):
        if request.user.is_authenticated:
            result = view(request, *args, **kwargs)
            return result
        return HttpResponseForbidden()
    return wrapper