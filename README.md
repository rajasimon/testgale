# Test Gale

## What I need to done next

I know this repo contains code for the coding challenge but I need to address a few things before you jump into my code. 

I integrated Django channels why because I thought I can implement async nature into the code so that it runs on the multiple threads. But Currently, my code only does 1 depth. And the frontend is very minimal it's done the only submission part. 

The React part serves from the internal server only don't need to run npm at all. 
And You need to follow these steps for a successful run. 

    redis-server
    pipenv install
    pipenv run python manage.py migrate
    pipenv run python manage.py runserver
    pipenv run python manage.py runworker crawler-process


