# BriteCore Test Project

# Backend

## Server Side
***Django 2*** with ***Python 3.6***, ***Postgres10*** and ***django rest framework*** was used in the backbone of the server. Several API endpoints (using the ***django rest framework***) and a single page view have been implemented as in the requirements. The deployment scheme used AWS services of ***S3***, ***Lambda***, ***RDS*** and ***Cloud Formation***. ***Zappa*** (along with ***virtualenv***) was used for the whole deployment process. Static files were served from ***S3*** bucket instance. 
Environment variable were used to separate the production settings from development settings. The command `source init_local_env.sh` is used to set local environment variables. The production environment variables are set for production in `zappa_settings.json`. 
Finaly, its worth noting that test data was generated using a custom written django managment command script named `createtestdata.py`. Further deployment options using ***Docker*** containers and ***gunicorn*** with ***whitenoise*** are also provided, see the end of this readme file for further details.

A working instance of the project can be found at: 
https://f2uddx7bli.execute-api.us-east-2.amazonaws.com/dev/


## Db Model

There are 7 models:
+ **User**
+ **RiskType**
+ **RiskInstance**
+ **FieldType**
+ **Field**
+ **FieldValue**
+ **EnumValue**

This is an ER diagram for the models:
![ER DIAGRAM IMAGE](https://github.com/rabihkodeih/britecoretest/blob/master/britecore_test_project_models.png)

The **User** model is the usual django auth user model, it is related to the **RiskType** model through a foreign key relation.

The **RiskType** model represents the type of risk we are interested in such as "Automobile", "Property", etc... It includes a single `name` field.

The **RiskInstance** model holds one instance of the insurance form for a certain risk type. Since each risk type is related to one user, so is a risk instance model through it's corresponding type. For simplicity, we have only addorned this model with a single field of `title`.

The **FIeldType** model represents the type of field to be inserted in the insurance policy form. It has a `name`, `regex_validator` and `nullable` fields which are fairly self-explanatory. The `name` field is used on the frontend side to render the appropriate type of widget for the field. Note that users can generate more types and specify their respective regex-validator. Currently ther are four standard field types in the test data of the project, namely: "Text", "Date", "Enum" and "Number". A regular expression validator field is included and is used in the server side (as well as client side) validation of form data upon updates.

The **Field** model represents the insurance policy field. It has a `name`, a `type`, a `risk_type` and an `order` field. The `type` field relates the field to the respective **FIeldType** model. The `risk_type` field relates the field to the **RiskType** model and finally the `order` field defines the order in which the field should be rendered in the corresponsing form. Note that the **Field** model has no `value` attribute. This is because this model is equivalent to the schema of the insurance policy form and thus we need another couple of models to represent the actual policy form instance along with its associated values (**RiskInstance** and **FieldValue**). This model also has a required field that is used in the UI to determine wether the user needs to fill in a value or not.

The **FieldValue** is a simple model that holds data of a field in a text data field. It is related both to **Field** and **RiskInstance**. A downside of this design is that searching for a field value in a large set of risk instances would require a join between several tables and thus makes use of compound indexes a necessity. However, this design also offers flexibilty in holding values of fields of any type.

Finally the **EnumValue** model represents the different enum values that are associated with a field of type "Enum" (or any equivalent type). Note that the alternative of relating this model to **FieldType** rather than **Field** wouldn't have made sense since this would have required a lot more field type records to add.


# Frontend

The whole frontend application was implemented in a single relatively small javascript file `app.js`. The reactive framework ***Vue.js*** was the main library used in the backend along with ***jquery3***, ***axios.js*** (promise based ajax calls), ***bootstrap4*** (for styling) and ***gijgo.js*** (used to render the date-picker widget). The modern flavor of ***JavaScript ES6*** has been used in `app.js`. The vue component reside in a separate `js\vue_components\` directory.

The main app was implemented using two components: one component to model the different field types and another component to model the date-widget. Note that django reversed url strings where injected in the javascript code instead of hardcoding api urls to allow the project to be deployed by zappa under different guises (*dev*, *staging*, *production*). A fully reactive model was used to render the main project page view. This proved to be very versatile as it greatly simplified the code of the app in comparison to using more traditional event-driven methods. Finaly, a *css* file was used to finetune some styling elements in the main page.

The app also includes basic user session management (login/logout, all views require authentication including those of the api) as well as some css fade transition effects. Additionaly, client side form data validation is provided.

This is a screenshot of the UI:
![UI_SCREENSHOT IMAGE](https://github.com/rabihkodeih/britecoretest/blob/master/UI_screenshot.png)


# Tests

A standard django test suite was employed. There are two test cases, one for login sessions and db models, the other for the api section.
To run test, simply issue:

    ./manage.py test


# Deployment with Zappa and AWS Lambda

After cloning this repository to a local workding directry and setting up a local working copy of the project, run the createtestdata command: 

    python manage.py createtestdata

This will create an initial set of data on the local server. Now make sure that the app is working correctly locally.

To deploy, just run the command 

    bash deploy_dev 

found on the root folder (this assumes that you allready have your AWS account settings correctly configured, to make sure edit the file `zappa_settings.js` and update the settings as required). The `deploy_dev` bash script contains all the necessary steps for the deployment including collecting static files and running the tests.

To create test data on the server, simply run the following command: 

    zappa manage dev createtestdata

This will create the initial test data as we have done on the local environment. Now everything should be ready, simply navigate to the production url and experiment.


# Installation on Local Dev Machine

First make sure that `Python3`, `pip3` and `virtualenv` are all installed and working fine:

    apt-get update
    apt-get dist-upgrade
    apt-get install -y python3-dev virtualenv gcc libmysqlclient-dev

Clone the repository into a destination directory, cd into it then create your virtual env using

    virtualenv -p python3 env
    
and activate it by

    . env/bin/activate
    
Now you can install the requirements by

    pip3 install -r requirements.txt
        
Set the environment variables as desired, example values are:

| Key                       | Value                |
| --------------------------| -------------------- |
| BC_SECRET_KEY | yf*e^dqt2b4^lnf8$1kqotk&2w!-ab!nc83jl$++g-ztn8xd^+ |
| BC_DEBUG | 1 |
| BC_DB_NAME | britecore |
| BC_DB_USER | postgres |
| BC_DB_PASSWORD | admin |
| BC_DB_HOST | localhost |
| BC_DB_PORT | 5432 |
| BC_STATIC_URL | /static/ 
| BC_STATICFILES_STORAGE | django.contrib.staticfiles.storage.StaticFilesStorage


In a plsql console, create the databases using the corresponding environment variables. 

Now create the admin related tables:

    ./manage.py makemigrations
    ./manage.py migrate
    
Before we can use the admin site, we need to create a superuser login and the test data:

    ./manage.py createsuperuser
    ./manage.py createtestdata


### Using Local Development Server 

Run the Django local server using:

    ./manage.py runserver
    
and visit `http://127.0.0.1:8000/admin/` or `http://127.0.0.1:8000/`.

    
### Using Gunicorn

Simply issue the following command from the root source folder:

    gunicorn britecore.wsgi:application \
        --name britecore_worker \
        --bind 0.0.0.0:8000 \
        --workers=1 \
        --daemon

If you don't want to run the server in daemon mode, remove the last option.

Now visit `http://127.0.0.1:8000/admin/` or `http://127.0.0.1:8000/`.


# Installation Using Docker Containers

Clone the repository into a project source folder, then build your image:

    cd <project source folder>
    docker build -t britecore .

When done, edit the file run_container.sh, which looks like this for example:

    #!/bin/bash
    docker run -it -p 8000:8000 \
    -e export BC_SECRET_KEY='yf*e^dqt2b4^lnf8$1kqotk&2w!-ab!nc83jl$++g-ztn8xd^+' \
    -e export BC_DEBUG=0 \
    -e export BC_DB_NAME=britecoretest \
    -e export BC_DB_USER=britecoretestadmin7bli \
    -e export BC_DB_PASSWORD=fhuryg^&^%3et64%&&*derrf2390 \
    -e export BC_DB_HOST=rds-postgresql-7bli.cth7mcrqx10m.us-east-2.rds.amazonaws.com \
    -e export BC_DB_PORT=5432 \
    -e export BC_STATIC_URL='https://zappa-static-7bli.s3.amazonaws.com/' \
    -e export BC_STATICFILES_STORAGE='storages.backends.s3boto.S3BotoStorage' \
    --name
    britecore:latest


and set the desired production values. Now run the container with:

    ./run_container.sh
    
To setup the database, create a database named `britecoretest` on your chosen database hosting machine.

Now connect to the container as follows:

    docker exec -it {container name} /bin/bash

then from the container bash terminal perform:

    ./manage.py makemigrations
    ./manage.py migrate
    ./manage.py createsuperuser
    ./manage.py createtestdata

and now you can visit the admin site in the container host machine at `http://127.0.0.1:8000/admin/`
or the main site at `http://127.0.0.1:8000/`.









