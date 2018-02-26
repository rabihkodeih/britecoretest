'''
Created on Feb 26, 2018

@author: rabihkodeih
'''

from django.test import TestCase
from django.contrib.auth.models import User
from django.test import Client
from main.models import RiskType
from main.models import FieldType
from main.models import Field
from main.models import EnumValue
from main.management.commands.createtestdata import Command


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
    
   
    def test_logins(self):
        '''
        This is a test for logins
        '''
        c = Client()
        response = c.login(username='phil', password='adminadmin')
        self.assertTrue(response)
        
        
    def test_models(self):
        '''
        This is a test to sanity check the database models
        '''
        self.assertEqual(len(RiskType.objects.all()), 4)
        self.assertEqual(len(FieldType.objects.all()), 4)
        self.assertEqual(len(Field.objects.all()), 20)
        self.assertEqual(len(EnumValue.objects.all()), 13)
        



