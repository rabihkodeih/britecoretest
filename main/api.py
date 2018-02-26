'''
Created on Feb 4, 2018

@author: rabihkodeih
'''
from django.http.response import JsonResponse
from django.urls.conf import path
from main.models import RiskType
from main.serializers import RiskTypeSerializer
from main.serializers import RiskTypeShallowSerializer
from main.decorators import requires_authentication
from rest_framework.decorators import api_view  # @UnresolvedImport


@api_view(["GET"])
@requires_authentication
def risktype(request, risktype_id=0):
    ''' 
    This api function is used to get a single risktype
    @param request: django request object
    @param risktype_id: the id of the risktype object to be returned
    @return: JSON object 
    '''
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
    ''' 
    This api function is used to get all risktypes associated with the current session user
    @param request: django request object
    @return: a list of JSON object 
    '''
    risktypes = RiskType.objects.filter(user=request.user).select_related()
    serializer = RiskTypeShallowSerializer(risktypes, many=True)
    data = serializer.data 
    return JsonResponse(data, safe=False)


urls = [path('risktype/<int:risktype_id>/', risktype, name='url_risktype_arg'),
        path('risktype/', risktype, name='url_risktype'),
        path('risktypes/', risktypes, name='url_risktypes')]
