'''
Created on Feb 4, 2018

@author: rabihkodeih
'''
from django.http.response import JsonResponse
from django.urls.conf import path
from main.models import RiskType 
from main.models import FieldValue
from main.models import RiskInstance
from main.serializers import RiskTypeSerializer, FieldSerializer,\
    FieldValueSerializer
from main.serializers import RiskInstanceSerializer
from main.serializers import RiskInstanceShallowSerializer
from main.decorators import requires_authentication
from rest_framework.decorators import api_view
from rest_framework.decorators import authentication_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authentication import BasicAuthentication
from main.utils import save_new_riskinstance


@requires_authentication
@api_view(["GET"])
def riskinstance_new(request, risktype_id=0):
    #TODO: insert doc string
    data = {}
    result = RiskType.objects.filter(id=risktype_id)
    if result:
        risktype = result[0]
        fields = risktype.fields.all()
        riskinstance = RiskInstance(id=0, title='', type=risktype)
        fieldvalues = [FieldValue(id=0, value='', field=f, riskinstance=riskinstance) for f in fields]
        columns_serializer = FieldValueSerializer(fieldvalues, many=True)
        data = RiskInstanceSerializer(riskinstance).data
        data['columns'] = columns_serializer.data
    return JsonResponse(data, safe=False)


@requires_authentication
@api_view(["GET"])
def riskinstance(request, riskinstance_id):
    #TODO: insert doc string
    data = {}
    result = RiskInstance.objects.filter(id=riskinstance_id)
    if result:
        riskinstance = result[0]
        serializer = RiskInstanceSerializer(riskinstance)
        data = serializer.data
    return JsonResponse(data, safe=False)
    

#TODO: imbed this save function with the above one
# @requires_authentication
# @api_view(["POST"])    
# @authentication_classes((BasicAuthentication,))
# def riskinstance(request):
#     #FIXME: add cocumentation
#     from pprint import pprint
#     pprint(request.data)
#     #FIXME: complete implementation
#     #save_new_riskinstance(request.data)
# #     serializer = SnippetSerializer(data=request.data)
# #     if serializer.is_valid():
# #         serializer.save()
# #     return Response(serializer.data, status=status.HTTP_201_CREATED)
#     return Response({}, status=status.HTTP_201_CREATED)
#     #return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@requires_authentication
@api_view(["GET"])
def risktypes(request):
    ''' 
    This api function is used to get all risktypes associated with the current session user
    @param request: django request object
    @return: a list of JSON object 
    '''
    risktypes = RiskType.objects.filter(user=request.user).select_related()
    serializer = RiskTypeSerializer(risktypes, many=True)
    data = serializer.data 
    return JsonResponse(data, safe=False)


@requires_authentication
@api_view(["GET"])
def riskinstances(request):
    ''' 
    This api function is used to get all riskinstances associated with the current session user
    @param request: django request object
    @return: a list of JSON object 
    '''
    riskinstances = RiskInstance.objects.filter(type__user=request.user).order_by('title').select_related()
    serializer = RiskInstanceShallowSerializer(riskinstances, many=True)
    data = serializer.data 
    return JsonResponse(data, safe=False)


urls = [path('risktypes/', risktypes, name='url_risktypes'),
        path('riskinstance_new/', riskinstance_new, name='url_riskinstance_new'),
        path('riskinstance_new/<int:risktype_id>/', riskinstance_new, name='url_riskinstance_new_arg'),
        path('riskinstance/<int:riskinstance_id>/', riskinstance, name='url_riskinstance_arg'),
        path('riskinstance/', riskinstance, name='url_riskinstance'),
        path('riskinstances/', riskinstances, name='url_riskinstances')]
