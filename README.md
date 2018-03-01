# BriteCore Test Project

# Backend

## Server Side
***Django v2.02*** with ***Python 3.6***, ***Postgres10*** and ***django rest framework*** was used in the backbone of the server. Two API endpoints (using the ***django rest framework***) and a single page view have been implemented as in the requirements. The deployment scheme used AWS services of ***S3***, ***Lambda***, ***RDS*** and ***CloudFront***. ***Zappa*** (along with ***virtualenv***) was used for the whole deployment process. Static files were served from ***S3*** bucket instance. A `local_settings.py` file was used to separate the local development settings from the production settings, this file isn't tracked by either ***zappa*** nor ***git***. Finaly, its worth noting that test data was generated using a custom written django managment command script named `createtestdata.py`.

A working instance of the project can be found at: 
https://f2uddx7bli.execute-api.us-east-2.amazonaws.com/dev/

## Db Model

There are four models:
+ **User**
+ **RiskType**
+ **FieldType**
+ **Field**
+ **EnumValue**

This is an ER diagram for the models:
![ER DIAGRAM IMAGE](https://github.com/rabihkodeih/britecoretest/blob/master/britecore_test_project_models.png)

The **User** model is the usual django auth user model, it is related to the **RiskType** model through a foreign key relation.

The **RiskType** model represents the type of risk we are interested in such as "Automobile", "Property", etc... It includes a single `name` field.

The **FIeldType** model represents the type of field to be inserted in the insurance policy form. It has a `name`, `regex_validator` and `nullable` fields which are fairly self-explanatory. The `name` field is used on the frontend side to render the appropriate type of widget for the field. Note that users can generate more types and specify their respective regex-validator. Currently ther are four standard field types in the test data of the project, namely: "Text", "Date", "Enum" and "Number".

The **Field** model represents the insurance policy field. It has a `name`, a `type`, a `risk_type` and an `order` field. The `type` field relates the field to the respective **FIeldType** model. The `risk_type` field relates the field to the **RiskType** model and finally the `order` field defines the order in which the field should be rendered in the corresponsing form. Note that the **Field** model has no `value` attribute. This is because this model is equivalent to the schema of the insurance policy form and thus we need another couple of models to represent the actual policy form instance along with its associated values.

Finally the **EnumValue** model represents the different enum values that are associated with a field of type "Enum" (or any equivalent type). Note that the alternative of relating this model to **FieldType** rather than **Field** wouldn't have made sense since this would have required a lot more field type records to add.

# Frontend

The whole frontend application was implemented in a single relatively small javascript file `app.js`. The reactive framework ***Vue.js*** was the main library used in the backend along with ***jquery3***, ***axios.js*** (promise based ajax calls), ***bootstrap4*** (for styling) and ***gijgo.js*** (used to render the date-picker widget). The modern flavor of ***JavaScript ES6*** has been used in `app.js`. The vue component reside in a separate `js\vue_components\` directory.

The main app was implemented using two components: one component to model the different field types and another component to model the date-widget. Note that django reversed url strings where injected in the javascript code instead of hardcoding api urls to allow the project to be deployed by zappa under different guises (*dev*, *staging*, *production*). A fully reactive model was used to render the main project page view. This proved to be very versatile as it greatly simplified the code of the app in comparison to using more traditional event-driven methods. Finaly, a *css* file was used to finetune some styling elements in the main page.

The app also includes basic user session management (login/logout, all views require authentication including those of the api).

# Tests

A standard django test suite was employed. There are two test cases, one for login sessions and db models, the other for the api section.

# Deployment

After cloning this repository to a local workding directry and setting up a local working copy of the project, run the createtestdata command: `python manage.py createtestdata`. This will create an initial set of data on the local server. Now make sure that the app is working correctly locally.

To deploy, just run the command `bash deploy_dev` found on the root folder (this assumes that you allready have your AWS account settings correctly configured, to make sure edit the file `zappa_settings.js` and update the settings as required). The `deploy_dev` bash script contains all the necessary steps for the deployment including collecting static files and running the tests.

To create test data on the server, simply run the following command: `zappa manage dev createtestdata`. This will create the initial test data as we have done on the local environment. Now everything should be ready, simply navigate to the production url and enjoy!
