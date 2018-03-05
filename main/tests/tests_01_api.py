'''
Created on Feb 26, 2018

@author: rabihkodeih
'''

import re
import json
from django.test import TestCase
from django.contrib.auth.models import User
from django.test import Client
from django.urls import reverse
from main.models import RiskType
from main.models import RiskInstance
from main.management.commands.createtestdata import Command as CreateTestData
from main.utils import populate_fields



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
        CreateTestData().handle()
        # logout from all accounts
        c = Client()
        c.logout()
 
 
    def test_endpoint_url_risktypes_unauthenticated(self):
        '''
        This test makes sure that unauthentcated calls to endpoint receive an HTTP 403 FORBIDDEN response.
        '''
        c = Client()
        response = c.get(reverse('url_risktypes'), follow=True)
        self.assertEqual(response.status_code, 403)


    def test_endpoint_url_risktypes_regular(self):
        '''
        This is a regular test for the endpoint which should return a nominal JSON response
        '''
        c = Client()
        c.login(username='phil', password='adminadmin')
        response = c.get(reverse('url_risktypes'), follow=True)
        nominal_response_content = b'''[{"id": 16, "name": "Automobile"}, {"id": 15, "name": "Property"}]'''
        self.assertEqual(response.status_code, 200)
        nominal_response_content = normalize_ids(nominal_response_content)
        response_content = normalize_ids(response.content)
        self.assertEqual(response_content, nominal_response_content)
        
        
    def test_endpoint_url_riskinstance_new_unauthenticated(self):
        '''
        This test makes sure that unauthentcated calls to endpoint receive an HTTP 403 FORBIDDEN response.
        '''
        c = Client()
        response = c.get(reverse('url_riskinstance_new'), follow=True)
        self.assertEqual(response.status_code, 403)

    
    def test_endpoint_url_riskinstance_new_empty(self):
        '''
        This tests that a a call to this endpoint without an argument returns an empty response
        '''
        c = Client()
        c.login(username='phil', password='adminadmin')
        response = c.get(reverse('url_riskinstance_new'), follow=True)
        nominal_response_content = b'''{}'''
        self.assertEqual(response.status_code, 200)
        nominal_response_content = normalize_ids(nominal_response_content)
        response_content = normalize_ids(response.content)
        self.assertEqual(response_content, nominal_response_content)
    
    
    def test_endpoint_url_riskinstance_new_regular(self):
        '''
        This tests that a a call to this endpoint with an argument returns a nominal JSON object
        '''
        c = Client()
        c.login(username='phil', password='adminadmin')
        risktype_id = RiskType.objects.get(name='Property').id
        response = c.get('%s%s' % (reverse('url_riskinstance_new'), risktype_id), follow=True)
        nominal_response_content = b'''{"id": 0, "title": "", "type": {"id": 15, "name": "Property"}, "columns": [{"value": "", "field": {"id": 71, "name": "Address", "type": {"id": 16, "name": "Text", "regex_validator": "^.*$", "nullable": true}, "required": true, "order": 1, "enum_values": []}}, {"value": "", "field": {"id": 72, "name": "ZipCode", "type": {"id": 16, "name": "Text", "regex_validator": "^.*$", "nullable": true}, "required": true, "order": 2, "enum_values": []}}, {"value": "", "field": {"id": 73, "name": "Property Type", "type": {"id": 13, "name": "Enum", "regex_validator": "^.*$", "nullable": false}, "required": false, "order": 3, "enum_values": [{"value": "Private Property"}, {"value": "Government Building"}, {"value": "Church"}, {"value": "Land"}]}}, {"value": "", "field": {"id": 74, "name": "Coverage B Limit", "type": {"id": 15, "name": "Number", "regex_validator": "^$|^-?[0-9]*\\\\.?[0-9]+$", "nullable": false}, "required": true, "order": 4, "enum_values": []}}, {"value": "", "field": {"id": 75, "name": "Date of Renewal", "type": {"id": 14, "name": "Date", "regex_validator": "^$|^\\\\d{2}/\\\\d{2}/\\\\d{4}$", "nullable": false}, "required": true, "order": 5, "enum_values": []}}]}'''
        self.assertEqual(response.status_code, 200)
        nominal_response_content = normalize_ids(nominal_response_content)
        response_content = normalize_ids(response.content)
        self.assertEqual(response_content, nominal_response_content)
    

    def test_endpoint_url_riskinstances_unauthenticated(self):
        '''
        This test makes sure that unauthentcated calls to endpoint receive an HTTP 403 FORBIDDEN response.
        '''
        c = Client()
        response = c.get(reverse('url_riskinstances'), follow=True)
        self.assertEqual(response.status_code, 403)


    def test_endpoint_url_riskinstances_regular(self):
        '''
        This tests that a a call to this endpoint with an argument returns a nominal JSON object
        '''
        c = Client()
        c.login(username='phil', password='adminadmin')
        response = c.get(reverse('url_riskinstances'), follow=True)
        nominal_response_content = b'''[{"id": 45, "title": "Automobile_7"}, {"id": 46, "title": "Automobile_8"}, {"id": 48, "title": "Property_10"}, {"id": 47, "title": "Property_9"}]'''
        self.assertEqual(response.status_code, 200)
        nominal_response_content = normalize_ids(nominal_response_content)
        response_content = normalize_ids(response.content)
        self.assertEqual(response_content, nominal_response_content)
    

    def test_endpoint_url_riskinstance_unauthenticated(self):
        '''
        This test makes sure that unauthentcated calls to endpoint receive an HTTP 403 FORBIDDEN response.
        '''
        c = Client()
        response = c.get(reverse('url_riskinstance'), follow=True)
        self.assertEqual(response.status_code, 403)


    def test_endpoint_url_riskinstance_empty(self):
        '''
        This tests that a a call to this endpoint without an argument returns an empty response
        '''
        c = Client()
        c.login(username='phil', password='adminadmin')
        response = c.get(reverse('url_riskinstance'), follow=True)
        nominal_response_content = b'''{}'''
        self.assertEqual(response.status_code, 200)
        nominal_response_content = normalize_ids(nominal_response_content)
        response_content = normalize_ids(response.content)
        self.assertEqual(response_content, nominal_response_content)

    
    def test_endpoint_url_riskinstance_regular(self):
        '''
        This tests that a a call to this endpoint with an argument returns a nominal JSON object
        '''
        c = Client()
        c.login(username='phil', password='adminadmin')
        riskinstance_id = RiskInstance.objects.get(title='Property_10').id
        response = c.get('%s%s' % (reverse('url_riskinstance'), riskinstance_id), follow=True)
        nominal_response_content = b'''{"id": 56, "title": "Property_10", "type": {"id": 27, "name": "Property"}, "columns": [{"value": "Central District Area Bock 5 str 22", "field": {"id": 131, "name": "Address", "type": {"id": 28, "name": "Text", "regex_validator": "^.*$", "nullable": true}, "required": true, "order": 1, "enum_values": []}}, {"value": 66455, "field": {"id": 132, "name": "ZipCode", "type": {"id": 28, "name": "Text", "regex_validator": "^.*$", "nullable": true}, "required": true, "order": 2, "enum_values": []}}, {"value": {"value": "Government Building"}, "field": {"id": 133, "name": "Property Type", "type": {"id": 25, "name": "Enum", "regex_validator": "^.*$", "nullable": false}, "required": false, "order": 3, "enum_values": [{"value": "Private Property"}, {"value": "Government Building"}, {"value": "Church"}, {"value": "Land"}]}}, {"value": 200000, "field": {"id": 134, "name": "Coverage B Limit", "type": {"id": 27, "name": "Number", "regex_validator": "^$|^-?[0-9]*\\\\.?[0-9]+$", "nullable": false}, "required": true, "order": 4, "enum_values": []}}, {"value": "04/30/2018", "field": {"id": 135, "name": "Date of Renewal", "type": {"id": 26, "name": "Date", "regex_validator": "^$|^\\\\d{2}/\\\\d{2}/\\\\d{4}$", "nullable": false}, "required": true, "order": 5, "enum_values": []}}]}'''
        self.assertEqual(response.status_code, 200)
        nominal_response_content = normalize_ids(nominal_response_content)
        response_content = normalize_ids(response.content)
        self.assertEqual(response_content, nominal_response_content)
        

    def test_endpoint_url_riskinstance_post_new(self):
        '''
        This tests that a a call to this endpoint creates a new risk instance
        '''
        c = Client()
        c.login(username='phil', password='adminadmin')
        risktype_id = RiskType.objects.get(name='Property').id
        response = c.get('%s%s' % (reverse('url_riskinstance_new'), risktype_id), follow=True)
        data = json.loads(response.content)
        data['title'] = 'Test'
        populate_fields(data, {'Address': 'address text',
                                'ZipCode': 'zipcode text',
                                'Property Type': {'value': 'Government Building'},
                                'Coverage B Limit': '1223344',
                                'Date of Renewal': '03/09/2018'})
        post_data = json.dumps(data)
        response = c.post(reverse('url_riskinstance'), data=post_data, follow=True, content_type='application/json')
        self.assertEqual(response.status_code, 201)
        riskinstance_id = RiskInstance.objects.get(title="Test").id
        response = c.get('%s%s' % (reverse('url_riskinstance'), riskinstance_id), follow=True)
        nominal_response_content = b'''{"id": 25, "title": "Test", "type": {"id": 11, "name": "Property"}, "columns": [{"value": "address text", "field": {"id": 51, "name": "Address", "type": {"id": 12, "name": "Text", "regex_validator": "^.*$", "nullable": true}, "required": true, "order": 1, "enum_values": []}}, {"value": "zipcode text", "field": {"id": 52, "name": "ZipCode", "type": {"id": 12, "name": "Text", "regex_validator": "^.*$", "nullable": true}, "required": true, "order": 2, "enum_values": []}}, {"value": {"value": "Government Building"}, "field": {"id": 53, "name": "Property Type", "type": {"id": 9, "name": "Enum", "regex_validator": "^.*$", "nullable": false}, "required": false, "order": 3, "enum_values": [{"value": "Private Property"}, {"value": "Government Building"}, {"value": "Church"}, {"value": "Land"}]}}, {"value": 1223344, "field": {"id": 54, "name": "Coverage B Limit", "type": {"id": 11, "name": "Number", "regex_validator": "^$|^-?[0-9]*\\\\.?[0-9]+$", "nullable": false}, "required": true, "order": 4, "enum_values": []}}, {"value": "03/09/2018", "field": {"id": 55, "name": "Date of Renewal", "type": {"id": 10, "name": "Date", "regex_validator": "^$|^\\\\d{2}/\\\\d{2}/\\\\d{4}$", "nullable": false}, "required": true, "order": 5, "enum_values": []}}]}'''
        self.assertEqual(response.status_code, 200)
        nominal_response_content = normalize_ids(nominal_response_content)
        response_content = normalize_ids(response.content)
        self.assertEqual(response_content, nominal_response_content)
        
    
    def test_endpoint_url_riskinstance_post_existing(self):
        '''
        This tests that a a call to this endpoint updates an existing risk instance
        '''
        c = Client()
        c.login(username='phil', password='adminadmin')
        riskinstance_id = RiskInstance.objects.get(title='Property_10').id
        response = c.get('%s%s' % (reverse('url_riskinstance'), riskinstance_id), follow=True)
        data = json.loads(response.content)
        data['title'] = 'Property_10s'
        populate_fields(data, {'Address': 'Central District Area Bock 5 str 23',
                                'ZipCode': '88244',
                                'Property Type': {'value': 'Church'},
                                'Coverage B Limit': '100300',
                                'Date of Renewal': '03/09/2019'})
        post_data = json.dumps(data)
        response = c.post(reverse('url_riskinstance'), data=post_data, follow=True, content_type='application/json')
        self.assertEqual(response.status_code, 201)
        response = c.get('%s%s' % (reverse('url_riskinstance'), riskinstance_id), follow=True)
        nominal_response_content = b'''{"id": 24, "title": "Property_10s", "type": {"id": 11, "name": "Property"}, "columns": [{"value": "Central District Area Bock 5 str 23", "field": {"id": 51, "name": "Address", "type": {"id": 12, "name": "Text", "regex_validator": "^.*$", "nullable": true}, "required": true, "order": 1, "enum_values": []}}, {"value": 88244, "field": {"id": 52, "name": "ZipCode", "type": {"id": 12, "name": "Text", "regex_validator": "^.*$", "nullable": true}, "required": true, "order": 2, "enum_values": []}}, {"value": {"value": "Church"}, "field": {"id": 53, "name": "Property Type", "type": {"id": 9, "name": "Enum", "regex_validator": "^.*$", "nullable": false}, "required": false, "order": 3, "enum_values": [{"value": "Private Property"}, {"value": "Government Building"}, {"value": "Church"}, {"value": "Land"}]}}, {"value": 100300, "field": {"id": 54, "name": "Coverage B Limit", "type": {"id": 11, "name": "Number", "regex_validator": "^$|^-?[0-9]*\\\\.?[0-9]+$", "nullable": false}, "required": true, "order": 4, "enum_values": []}}, {"value": "03/09/2019", "field": {"id": 55, "name": "Date of Renewal", "type": {"id": 10, "name": "Date", "regex_validator": "^$|^\\\\d{2}/\\\\d{2}/\\\\d{4}$", "nullable": false}, "required": true, "order": 5, "enum_values": []}}]}'''
        self.assertEqual(response.status_code, 200)
        nominal_response_content = normalize_ids(nominal_response_content)
        response_content = normalize_ids(response.content)
        self.assertEqual(response_content, nominal_response_content)
    
        
    def test_endpoint_url_riskinstance_delete(self):
        '''
        This tests that a a call to this endpoint deletes an existing risk instance
        '''
        c = Client()
        c.login(username='phil', password='adminadmin')
        riskinstance_id = RiskInstance.objects.get(title='Property_9').id
        data = {'ri_id': riskinstance_id}
        delete_data = json.dumps(data)
        response = c.delete(reverse('url_riskinstance'), data=delete_data, follow=True, content_type='application/json')
        self.assertEqual(response.status_code, 200)
        result = RiskInstance.objects.filter(id=riskinstance_id)
        self.assertEqual(list(result), [])
        
        
    
        
    
    
    



