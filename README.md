# Test Gale

The Crawler core designed in a way that it can handle N number of depth. To 
achieve that it uses Django Channels to schedule tasks.

When user making the query with url and depth it will schedule new task for the
crawler. And then crawler pickes it up and start crawling the page. At the same
time it will save the url and depth. 

Once the page is scrapped and using Beautifulsoup it will get all the links and pages
for the current page and save those links and images to current database. 

The thing about the crawler is this runs on while loop and it will reduce the depth
each time it runs. So next time it runs it will ask about child links and store 
links and images separately.

The React part serves from the internal server only don't need to run npm at all. 
And You need to follow these steps for a successful run. 

    redis-server
    pipenv install
    pipenv run python manage.py migrate
    pipenv run python manage.py runserver
    pipenv run python manage.py runworker crawler-process


