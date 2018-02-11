'''
Created on Feb 4, 2018

@author: rabihkodeih
'''
from django.http.response import JsonResponse
from django.urls.conf import path
from django.views.decorators.http import require_http_methods
from main.models import RiskType


@require_http_methods(["GET"])
def risktype(request, risktype_id=0):
    result = RiskType.objects.filter(id=risktype_id)
    if result:
        risktype = result[0]
        data = risktype.serialize()
    else:
        data = {}    
    return JsonResponse(data, safe=True, content_type='application/json')


@require_http_methods(["GET"])
def risktypes(request):
    risktypes = RiskType.objects.select_related().order_by('name')
    data = RiskType.serialize_all()
    return JsonResponse(data, safe=False, content_type='application/json')


urls = [path('risktype/<int:risktype_id>/', risktype, name='url_risktype_arg'),
        path('risktype/', risktype, name='url_risktype'),
        path('risktypes/', risktypes, name='url_risktypes')]
