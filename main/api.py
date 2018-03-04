'''
Created on Feb 4, 2018

@author: rabihkodeih
'''
from django.http.response import JsonResponse
from django.urls.conf import path
from main.models import RiskType 
from main.models import FieldValue
from main.models import RiskInstance
from main.serializers import RiskTypeSerializer
from main.serializers import FieldValueSerializer
from main.serializers import RiskInstanceSerializer
from main.serializers import RiskInstanceShallowSerializer
from main.decorators import requires_authentication
from rest_framework.decorators import api_view
from rest_framework.decorators import authentication_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authentication import BasicAuthentication
from main.utils import save_riskinstance 
from main.utils import validate_riskinstance
from django.db import transaction
from django.db import IntegrityError
from django.db import DatabaseError


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
@api_view(["GET", "POST"])
@authentication_classes((BasicAuthentication,))
def riskinstance(request, riskinstance_id=0):
    #TODO: insert doc string
    if request.method == "GET":
        data = {}
        result = RiskInstance.objects.filter(id=riskinstance_id)
        if result:
            riskinstance = result[0]
            serializer = RiskInstanceSerializer(riskinstance)
            data = serializer.data
        return JsonResponse(data, safe=False)
    elif request.method == "POST":
        response = Response({}, status=status.HTTP_201_CREATED)
        if not validate_riskinstance(request.data):
            response = Response({'message': 'Could not validate form data'}, status=status.HTTP_406_NOT_ACCEPTABLE)
        else:
            try:
                with transaction.atomic():
                    save_riskinstance(request.data)
            except IntegrityError as er:
                message = 'There is another risk form with the same title.\nPlease chose another title.' 
                response = Response({'message': message}, status=status.HTTP_406_NOT_ACCEPTABLE)
            except Exception:
                response = Response({}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return response
    return Response({}, status=status.HTTP_400_BAD_REQUEST)
    

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
