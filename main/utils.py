'''
Created on Mar 2, 2018

@author: rabihkodeih
'''

import re
from main.models import RiskInstance
from main.models import FieldValue

# {'columns': [{'field': {'enum_values': [],
#                         'id': 151,
#                         'name': 'Ammount',
#                         'order': 1,
#                         'required': True,
#                         'type': {'id': 52,
#                                  'name': 'Number',
#                                  'nullable': False,
#                                  'regex_validator': '^$|^-?[0-9]*\\.?[0-9]+$'}},
#               'value': 1223},
#              {'field': {'enum_values': [{'value': 'Major'}, {'value': 'Minor'}],
#                         'id': 156,
#                         'name': 'Prize Type',
#                         'order': 6,
#                         'required': True,
#                         'type': {'id': 50,
#                                  'name': 'Enum',
#                                  'nullable': False,
#                                  'regex_validator': '^.*$'}},
#               'value': {'value': 'Major'}}],
#  'id': 3,
#  'title': 'Prize_3',
#  'type': {'id': 31, 'name': 'Prize'}}

def save_riskinstance(data):
    '''
    Saves a RiskInstance model object along with associated FieldValue objects.
    @param data: the riskinstance data to be saved
    @return: None
    '''
    rid = data['id']
    title = data['title']
    type_id = data['type']
    result = RiskInstance.objects.filter(id=rid)
    riskinstance = result[0] if result else RiskInstance(type_id=type_id)
    riskinstance.title = title
    riskinstance.save()
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
    
    

        
        