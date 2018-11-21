from django.core.management.base import BaseCommand
from main.models import EnumValue
from main.models import RiskType
from main.models import FieldType
from main.models import Field
from main.models import RiskInstance
from main.models import FieldValue
from django.contrib.auth.models import User


FIELDTYPES = [('Enum', r'^.*$', False),
              ('Date', r'^$|^\d{2}/\d{2}/\d{4}$', False),
              ('Number', r'^$|^-?[0-9]*\.?[0-9]+$', False),
              ('Text', r'^.*$', True)]


RISKTYPES = [{'name': 'CyberLiabilityCoverage',
              'username': 'rabih',
              'fields': [('Type of Coverage', 'Enum', ('DDOS Attack', 'Compromise of Credentials', 'Malware Infection'),
                          True),
                         ('Customer Name', 'Text', (), True),
                         ('Coverage Limit', 'Number', (), True),
                         ('Starting Date', 'Date', (), False)]},
             {'name': 'Prize',
              'username': 'rabih',
              'fields': [('Ammount', 'Number', (), True),
                         ('Customer Name', 'Text', (), False),
                         ('Customer Age', 'Number', (), True),
                         ('Coverage Limit', 'Number', (), True),
                         ('Due Date', 'Date', (), False),
                         ('Prize Type', 'Enum', ('Major', 'Minor'), True)]},
             {'name': 'Property',
              'username': 'phil',
              'fields': [('Address', 'Text', (), True),
                         ('ZipCode', 'Text', (), True),
                         ('Property Type', 'Enum', ('Private Property', 'Government Building', 'Church', 'Land'),
                          False),
                         ('Coverage B Limit', 'Number', (), True),
                         ('Date of Renewal', 'Date', (), True)]},
             {'name': 'Automobile',
              'username': 'phil',
              'fields': [('Brand', 'Text', (), True),
                         ('Automobile Type', 'Enum', ('Car', 'Truck', 'Minivan', 'Motorbike'), False),
                         ('Customer Name', 'Text', (), False),
                         ('Coverage Limit', 'Number', (), True),
                         ('Expiry Date', 'Date', (), False)]}]

RISKINSTANCES = [{'title': 'Prize_3',
                  'type': 'Prize',
                  'values': [1223, 'Jhon Doe', 33, 23, '03/21/2018', "{'value': 'Major'}"]},
                 {'title': 'Prize_4',
                  'type': 'Prize',
                  'values': [6653, 'Rabih Kodeih', 42, 5000, '03/16/2018', "{'value': 'Minor'}"]},
                 {'title': 'CyberLiabilityCoverage_5',
                  'type': 'CyberLiabilityCoverage',
                  'values': ["{'value': 'Compromise of Credentials'}", 'AEG', 25000, "03/17/2018"]},
                 {'title': 'CyberLiabilityCoverage_6',
                  'type': 'CyberLiabilityCoverage',
                  'values': ["{'value': 'DDOS Attack'}", "Central Bank", 75000, "05/23/2018"]},
                 {'title': 'Automobile_7',
                  'type': 'Automobile',
                  'values': ['BMW', "{'value': 'Car'}", 'Hala Sabbah', 12000, "04/11/2018"]},
                 {'title': 'Automobile_8',
                  'type': 'Automobile',
                  'values': ['Audi', "{'value': 'Truck'}", 'Daniel King', 65400, "04/27/2018"]},
                 {'title': 'Property_9',
                  'type': 'Property',
                  'values': ['21 Street Avenue Beirut', '882345', "{'value': 'Private Property'}",
                             33455, "05/14/2018"]},
                 {'title': 'Property_10',
                  'type': 'Property',
                  'values': ['Central District Area Bock 5 str 22', '66455', "{'value': 'Government Building'}",
                             200000, "04/30/2018"]}]


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
            except Exception:
                message = ('Could not create test data, user with username "%s" does'
                           ' not exit. Please create this user and try again.')
                self.stdout.write(self.style.ERROR(message % username))
                return
            risktype = RiskType(name=name, user=user)
            risktype.save()
            for ith, (name, field_type_name, enum_values, required) in enumerate(fields):
                field_type = FieldType.objects.get(name=field_type_name)
                field = Field(name=name,
                              type=field_type,
                              risk_type=risktype,
                              order=ith + 1,
                              required=required)
                field.save()
                for ith, enum_value in enumerate(enum_values):
                    EnumValue(field=field, value=enum_value, order=ith+1).save()
        for ri in RISKINSTANCES:
            risktype = RiskType.objects.get(name=ri['type'])
            riskinstance = RiskInstance(title=ri['title'], type=risktype)
            riskinstance.save()
            for f, v in zip(risktype.fields.all(), ri['values']):
                FieldValue(riskinstance=riskinstance, field=f, value=v).save()

        self.stdout.write(self.style.SUCCESS('Test data created successfully'))


# end of file
