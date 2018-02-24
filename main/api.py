'''
Created on Feb 4, 2018

@author: rabihkodeih
'''
from django.http.response import JsonResponse
from django.urls.conf import path
from main.models import RiskType
from main.serializers import RiskTypeSerializer, RiskTypeShallowSerializer
from rest_framework.decorators import api_view  # @UnresolvedImport
from main.decorators import requires_authentication



@api_view(["GET"])
@requires_authentication
def risktype(request, risktype_id=0):
    data = {}
    result = RiskType.objects.filter(id=risktype_id)
    if result:
        risktype = result[0]
        serializer = RiskTypeSerializer(risktype)
        data = serializer.data
    return JsonResponse(data, safe=False)


@api_view(["GET"])
@requires_authentication
def risktypes(request):
    risktypes = RiskType.objects.filter(user=request.user).select_related()
    serializer = RiskTypeShallowSerializer(risktypes, many=True)
    data = serializer.data 
    return JsonResponse(data, safe=False)


urls = [path('risktype/<int:risktype_id>/', risktype, name='url_risktype_arg'),
        path('risktype/', risktype, name='url_risktype'),
        path('risktypes/', risktypes, name='url_risktypes')]
