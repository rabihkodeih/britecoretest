# BriteCore Test Project

# Backend

## Server Side
***Django v2.02*** with ***Python 3.6*** and ***Postgres10*** was used as the backbone of the server. Two API endpoints have and a single page view have been implemented as in the requirements. The deployment scheme used AWS services of ***S3***, ***Lambda***, ***RDS*** and ***CloudFront***. ***Zappa*** (along with ***virtualenv***) was used for the whole deployment process. Static files were served from ***S3*** bucket instance. A `local_settings.py` file was used to separate the local development settings from the production settings, this file isn't tracked by either ***zappa*** nor ***git***. Finaly, its worth noting that test data was generated using a custom written django managment command script named `createtestdata.py`.

A working instance of the project can be found at: 
https://f2uddx7bli.execute-api.us-east-2.amazonaws.com/dev/

## Db Model

There are four models:
+ **RiskType**
+ **FieldType**
+ **Field**
+ **EnumValue**

The **RiskType** model represents the type of risk we are interested in such as "Automobile", "Property", etc... It includes a single `name` field.

The **FIeldType** model represents the type of field to be inserted in the insurance policy form. It has a `name`, `regex_validator` and `nullable` fields which are fairly self-explanatory. The `name` field is used on the frontend side to render the appropriate type of widget for the field. Note that users can generate more types and specify their respective regex-validator. Currently ther are four standard field types in the test data of the project, namely: "Text", "Date", "Enum" and "Number".

The **Field** model represents the insurance policy field. It has a `name`, a `type`, a `risk_type` and an `order` field. The `type` field relates the field to the respective **FIeldType** model. The `risk_type` field relates the field to the **RiskType** model and finally the `order` field defines the order in which the field should be rendered in the corresponsing form. Note that the **Field** model has no `value` attribute. This is because this model is equivalent to the schema of the insurance policy form and thus we need another couple of models to represent the actual policy form instance along with its associated values.

Finally the **EnumValue** model represents the different enum values that are associated with a field of type "Enum" (or any equivalent type). Note that the alternative of relating this model to **FieldType** rather than **Field** wouldn't have made sense since this would have required a lot more field type records to add.

# Frontend

The whole frontend application was implemented in a single relatively small javascript file `app.js`. The reactive framework ***Vue.js*** was the main library used in the backend along with ***jquery3***, ***axios.js*** (promise based ajax calls), ***bootstrap4*** (for styling) and ***gijgo.js*** (used to render the date-picker widget). 

The main app was implemented using two components: one component to model the different field types and another component to model the date-widget. Note that django reversed url strings where injected in the javascript code instead of hardcoding api urls to allow the project to be deployed by zappa under different guises (*dev*, *staging*, *production*). A fully reactive model was used to render the main project page view. This proved to be very versatile as it greatly simplified the code of the app in comparison to using more traditional event-driven methods. Finaly, a *css* file was used to finetune some styling elements in the main page.
