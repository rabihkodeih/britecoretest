from django.urls.conf import path
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views import View
from britecore.settings import LOGIN_URL


class MainView(View):
    @method_decorator(login_required(login_url=LOGIN_URL))
    def get(self, request):
        context = {}
        return render(request, 'home.html', context)


urls = [path('', MainView.as_view(), name='url_default'),
        path('home/', MainView.as_view(), name='url_home')]


# end of file
