'''
Created on Feb 26, 2018

@author: rabihkodeih
'''

import re
from django.test import TestCase
from django.contrib.auth.models import User
from django.test import Client
from main.models import RiskType
from main.management.commands.createtestdata import Command


def normalize_ids(text):
    '''
    This function normalizes the id values to -1 of the JSON response strings
    @param text: the input test string
    @return: a string object with ids normalized to -1
    '''
    return re.sub(r'"id"\s*:\s*\d+', r'"id": -1', str(text))


class APITestCase(TestCase):
    def setUp(self):
        '''
        This sets up the environment prior to each test. The setup includes things like database filling with test data and
        configuring various sysem parameters, or session initialization for example.
        '''
        # create test users:
        User.objects.create_user(username='rabih', email='rabih@britecore.com', password='adminadmin')
        User.objects.create_user(username='phil', email='phil@britecore.com', password='adminadmin')
        # setup the test database using the createtestdata command
        Command().handle()
        # logout from all accounts
        c = Client()
        c.logout()

    
    def test_endpoint_url_risktype_unauthenticated(self):
        '''
        This test makes sure that unauthentcated calls to endpoint receive an HTTP 403 FORBIDDEN response.
        '''
        risktype_ids = [r.id for r in RiskType.objects.all()]
        c = Client()
        for risktype_id in risktype_ids:
            response = c.get('/api/risktype/%s' % risktype_id, follow=True)
            self.assertEqual(response.status_code, 403)
            

    def test_endpoint_url_risktype_not_found(self):
        '''
        This test is for endpoint calls for a nonexisting risktype id
        '''
        risktype_ids = [r.id for r in RiskType.objects.all()]
        nonexisting_risktype_id = max(risktype_ids) + 1
        c = Client()
        c.login(username='phil', password='adminadmin')
        response = c.get('/api/risktype/%s' % nonexisting_risktype_id, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content, b'{}')
        
 
    def test_endpoint_url_risktype_regular(self):
        '''
        This is a regular test for the endpoint which should return a nominal JSON response
        '''
        risktype_id = RiskType.objects.get(name='Automobile').id
        c = Client()
        c.login(username='phil', password='adminadmin')
        response = c.get('/api/risktype/%s' % risktype_id, follow=True)
        nominal_response_content = b'''{"id": 8, "name": "Automobile", "fields": [{"id": 36, "name": "Brand", "type": {"id": 8, "name": "Text", "regex_validator": ".*", "nullable": true}, "order": 1, "enum_values": []}, {"id": 37, "name": "Automobile Type", "type": {"id": 5, "name": "Enum", "regex_validator": ".+", "nullable": false}, "order": 2, "enum_values": [{"value": "Car"}, {"value": "Truck"}, {"value": "Minivan"}, {"value": "Motorbike"}]}, {"id": 38, "name": "Customer Name", "type": {"id": 8, "name": "Text", "regex_validator": ".*", "nullable": true}, "order": 3, "enum_values": []}, {"id": 39, "name": "Coverage Limit", "type": {"id": 7, "name": "Number", "regex_validator": "[-.0-9]+", "nullable": false}, "order": 4, "enum_values": []}, {"id": 40, "name": "Expiry Date", "type": {"id": 6, "name": "Date", "regex_validator": "\\\\d{4}-\\\\d{2}-\\\\d{2}", "nullable": false}, "order": 5, "enum_values": []}]}'''
        self.assertEqual(response.status_code, 200)
        # ids may change so we normalize them here in the test strings
        nominal_response_content = normalize_ids(nominal_response_content)
        response_content = normalize_ids(response.content)
        self.assertEqual(response_content, nominal_response_content)
 
 
    def test_endpoint_url_risktypes_unauthenticated(self):
        '''
        This test makes sure that unauthentcated calls to endpoint receive an HTTP 403 FORBIDDEN response.
        '''
        c = Client()
        response = c.get('/api/risktypes/', follow=True)
        self.assertEqual(response.status_code, 403)


    def test_endpoint_url_risktypes_regular(self):
        '''
        This is a regular test for the endpoint which should return a nominal JSON response
        '''
        c = Client()
        c.login(username='phil', password='adminadmin')
        response = c.get('/api/risktypes/', follow=True)
        nominal_response_content = b'''[{"id": 16, "name": "Automobile"}, {"id": 15, "name": "Property"}]'''
        self.assertEqual(response.status_code, 200)
        # ids may change so we normalize them here in the test strings
        nominal_response_content = normalize_ids(nominal_response_content)
        response_content = normalize_ids(response.content)
        self.assertEqual(response_content, nominal_response_content)
        
