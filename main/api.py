'''
Created on Feb 4, 2018

@author: rabihkodeih
'''
from django.http.response import JsonResponse
from django.urls.conf import path
from django.views.decorators.http import require_http_methods
from main.models import RiskType

#TODO: setup a VPC (pattern: VPC with a Public subnet and Private subnet)
#TODO: setup the database
#TODO: write a command to fill in the database with the test data, and run this command using zappa on the lambda instance

#TODO: fix the group selection for enums

#TODO: generate ER model using the tool that is used in tms school django app
#TODO: write a comprehensive readme.txt file that explains everything (github readme file better)
#        mention that error checking was removed for brevity
#        mention something about the Virtual Private Cloud (VPC) (it must be usef for more security etc...)
#        mention that all regions are: US East (Ohio), (us-east-2)

#TODO: test on different agents from the developer menu in safari
#TODO: test form different machines


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
