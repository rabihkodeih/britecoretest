from django.db import transaction
from django.db import IntegrityError
from django.urls.conf import path
from django.http.response import JsonResponse
from django.utils.decorators import method_decorator

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authentication import BasicAuthentication

from main.utils import save_riskinstance
from main.utils import validate_riskinstance
from main.models import RiskType
from main.models import FieldValue
from main.models import RiskInstance
from main.decorators import requires_authentication
from main.serializers import RiskTypeSerializer
from main.serializers import FieldValueSerializer
from main.serializers import RiskInstanceSerializer
from main.serializers import RiskInstanceShallowSerializer

import logging


logger = logging.getLogger(__name__)


class NewRiskInstanceApiHandler(APIView):

    @method_decorator(requires_authentication)
    def get(self, request, risktype_id=0):  # @UnusedVariable
        '''
        This api function is used to get a JSON object for a new riskinstance.
        @param risktype_id: the id of the risktype to be used in creating the risk instance
        @return: a JSON object
        '''
        data = {}
        result = RiskType.objects.filter(id=risktype_id)
        if result:
            risktype = result[0]
            fields = risktype.fields.all()
            riskinstance = RiskInstance(id=0, title='', type=risktype)
            fieldvalues = [FieldValue(id=0, value='', field=f, riskinstance=riskinstance)
                           for f in fields]
            columns_serializer = FieldValueSerializer(fieldvalues, many=True)
            data = RiskInstanceSerializer(riskinstance).data
            data['columns'] = columns_serializer.data
        return JsonResponse(data, safe=False)


class RiskInstanceApiHandler(APIView):
    authentication_classes = (BasicAuthentication,)

    def get(self, request, riskinstance_id=0):  # @UnusedVariable
        '''
        This api function is used to retreive a riskinstance.
        @param riskinstance_id: the id of the riskinstance object
        @return: JSON object in case 1, and HTTP response object in cases 2 and 3
        '''
        data = {}
        result = RiskInstance.objects.filter(id=riskinstance_id)
        if result:
            riskinstance = result[0]
            serializer = RiskInstanceSerializer(riskinstance)
            data = serializer.data
        return JsonResponse(data, safe=False)

    def post(self, request, riskinstance_id=0):  # @UnusedVariable
        '''
        This api function is used to save a riskinstance.
        @param riskinstance_id: the id of the riskinstance object
        @return: JSON object in case 1, and HTTP response object in cases 2 and 3
        '''
        response = Response({}, status=status.HTTP_201_CREATED)
        if not validate_riskinstance(request.data):
            response = Response({'message': 'Could not validate form data'}, status=status.HTTP_406_NOT_ACCEPTABLE)
        else:
            try:
                with transaction.atomic():
                    save_riskinstance(request.data)
            except IntegrityError:
                message = 'There is another risk form with the same title.\nPlease chose another title.'
                response = Response({'message': message}, status=status.HTTP_406_NOT_ACCEPTABLE)
            except Exception:
                logger.error(request.data)
                logging.exception('')
                response = Response({}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return response

    def delete(self, request, riskinstance_id=0):  # @UnusedVariable
        '''
        This api function is used to delete a riskinstance.
        @param riskinstance_id: the id of the riskinstance object
        @return: JSON object in case 1, and HTTP response object in cases 2 and 3
        '''
        response = Response({}, status=status.HTTP_200_OK)
        try:
            ri_id = request.data['ri_id']
            result = RiskInstance.objects.filter(id=ri_id)
            if result:
                riskinstance = result[0]
                riskinstance.delete()
            else:
                response = Response({}, status=status.HTTP_204_NO_CONTENT)
        except Exception:
            logger.error(request.data)
            logging.exception('')
            response = Response({}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return response


class RiskTypesApiHandler(APIView):

    @method_decorator(requires_authentication)
    def get(self, request):
        '''
        This api function is used to get all risktypes associated with the current session user
        @param request: django request object
        @return: a list of JSON object
        '''
        risktypes = RiskType.objects.filter(user=request.user).select_related()
        serializer = RiskTypeSerializer(risktypes, many=True)
        data = serializer.data
        return JsonResponse(data, safe=False)


class RiskInstancesApiHandler(APIView):

    @method_decorator(requires_authentication)
    def get(self, request):
        '''
        This api function is used to get all riskinstances associated with the current session user
        @param request: django request object
        @return: a list of JSON object
        '''
        riskinstances = RiskInstance.objects.filter(type__user=request.user).order_by('title').select_related()
        serializer = RiskInstanceShallowSerializer(riskinstances, many=True)
        data = serializer.data
        return JsonResponse(data, safe=False)


urls = [
    path('risktypes/', RiskTypesApiHandler.as_view(), name='url_risktypes'),
    path('riskinstance_new/', NewRiskInstanceApiHandler.as_view(), name='url_riskinstance_new'),
    path('riskinstance_new/<int:risktype_id>/', NewRiskInstanceApiHandler.as_view(), name='url_riskinstance_new_arg'),
    path('riskinstance/<int:riskinstance_id>/', RiskInstanceApiHandler.as_view(), name='url_riskinstance_arg'),
    path('riskinstance/', RiskInstanceApiHandler.as_view(), name='url_riskinstance'),
    path('riskinstances/', RiskInstancesApiHandler.as_view(), name='url_riskinstances')
]


# end of file
