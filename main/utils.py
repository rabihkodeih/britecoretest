'''
Created on Mar 2, 2018

@author: rabihkodeih
'''

from main.models import RiskInstance
from main.models import FieldValue


def save_new_riskinstance(data):
    risktype_name = data['name']
    risktype_id = data['id']
    riskinstance = RiskInstance(title=risktype_name, type_id=risktype_id)
    riskinstance.save()
    riskinstance.title = '%s_%s' % (riskinstance.title, riskinstance.id)
    riskinstance.save()
    for field in data['fields']:
        FieldValue(field_id=field['id'], 
                   riskinstance_id=riskinstance.id, 
                   holder=field['value']).save()
    
    

        
        