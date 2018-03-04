'''
Created on Mar 2, 2018

@author: rabihkodeih
'''

import re
from main.models import RiskInstance
from main.models import FieldValue


def save_riskinstance(data):
    '''
    Saves a RiskInstance model object along with associated FieldValue objects.
    @param data: the riskinstance data to be saved
    @return: None
    '''
    rid = data['id']
    title = data['title'].strip()
    type_id = data['type']['id']
    result = RiskInstance.objects.filter(id=rid)
    riskinstance = result[0] if result else RiskInstance(type_id=type_id)
    riskinstance.title = title
    riskinstance.save()
    rid = riskinstance.id
    for col in data['columns']:
        value, field_id = str(col['value']).strip(), col['field']['id']
        result = FieldValue.objects.filter(field_id=field_id, riskinstance_id=rid)
        fieldvalue = result[0] if result else FieldValue(field_id=field_id, riskinstance_id=rid)
        fieldvalue.value = value
        fieldvalue.save()


def validate_riskinstance(data):
    '''
    Validates a RiskInstance model data.
    @param data: the riskinstance data to be saved
    @return: True if validation is successfull or False otherwise
    '''
    result = True
    if data['title'].strip() == '':
        result = False
    else:
        for col in data['columns']:
            value, field = col['value'], col['field']
            if type(value) == dict: value = value['value']
            value = str(value).strip()
            if field['required'] and value == '': 
                result = False
                break
            if re.match(field['type']['regex_validator'], value) == None:
                result = False
                break
    return result
    
    

        
        