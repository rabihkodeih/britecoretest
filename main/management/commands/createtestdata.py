'''
Created on Feb 9, 2018

@author: rabihkodeih
'''

from django.core.management.base import BaseCommand
from main.models import EnumValue, RiskType, FieldType, Field
from django.contrib.auth.models import User


FIELDTYPES = [('Enum', r'.+', False),
              ('Date', r'\d{4}-\d{2}-\d{2}', False),
              ('Number', r'[-.0-9]+', False),
              ('Text', r'.*', True)]


RISKTYPES = [{'name': 'CyberLiabilityCoverage',
              'username': 'rabih',
              'fields': [('Type of Coverage', 'Enum', ('DDOS Attack', 'Compromise of Credentials', 'Malware Infection')),        
                         ('Customer Name', 'Text', ()),
                         ('Coverage Limit', 'Number', ()),
                         ('Starting Date', 'Date', ())]},
             {'name': 'Prize',
              'username': 'rabih',
              'fields': [('Ammount', 'Number', ()),
                         ('Customer Name', 'Text', ()),
                         ('Customer Age', 'Number', ()),
                         ('Coverage Limit', 'Number', ()),
                         ('Due Date', 'Date', ()),
                         ('Prize Type', 'Enum', ('Major', 'Minor'))]},
             {'name': 'Property',
              'username': 'phil',
              'fields': [('Address', 'Text', ()),
                         ('ZipCode', 'Text', ()),
                         ('Property Type', 'Enum', ('Private Property', 'Government Building', 'Church', 'Land')),
                         ('Coverage B Limit', 'Number', ()),
                         ('Date of Renewal', 'Date', ())]},
             {'name': 'Automobile',
              'username': 'phil',
              'fields': [('Brand', 'Text', ()),
                         ('Automobile Type', 'Enum', ('Car', 'Truck', 'Minivan', 'Motorbike')),
                         ('Customer Name', 'Text', ()),
                         ('Coverage Limit', 'Number', ()),
                         ('Expiry Date', 'Date', ())]}]


class Command(BaseCommand):
    help = 'Creates some test data'
    
    def handle(self, *args, **options):
        
        # delete all existing
        EnumValue.objects.all().delete()
        RiskType.objects.all().delete()
        Field.objects.all().delete()
        FieldType.objects.all().delete()
        
        # creat the actual test data
        for name, regex_validator, nullable in FIELDTYPES:
            FieldType(name=name, regex_validator=regex_validator, nullable=nullable).save()
            
        for risktype in RISKTYPES:
            name = risktype['name']
            username = risktype['username']
            fields = risktype['fields']
            try:
                user = User.objects.get(username=username)
            except:
                message = 'Could not create test data, user with username "%s" does not exit. Please create this user and try again.'
                self.stdout.write(self.style.ERROR(message % username))
                exit()
            risktype = RiskType(name=name, user=user)
            risktype.save()
            for ith, (name, field_type_name, enum_values) in enumerate(fields):
                field_type = FieldType.objects.get(name=field_type_name)
                field = Field(name=name, type=field_type, risk_type=risktype, order=ith+1)
                field.save()                
                for ith, enum_value in enumerate(enum_values):
                    EnumValue(field=field, value=enum_value, order=ith+1).save()
        
        self.stdout.write(self.style.SUCCESS('Test data created successfully'))






