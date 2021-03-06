# Book API
This folder contains an API and an virtualenv.

To copy this branch and work with the API, please follow the steps below:

* Create a folder to copy the branch.
* Clone the repository: `git clone https://github.com/bounswe/bounswe2017group7.git`
* Go into the folder: `cd bounswe2017group7`
* See all the branches: `git branch -a`
* Checkout to any branch you want to see: `git checkout origin/<branch_name>`
* Fetch the current files: `git fetch`

Now you have all the data in your local.  
* Move into the folder of the api: `cd 'Book API Homework'`  
* Activate the environment: `source env/bin/activate`
* Go into the bookapi folder: `cd bookapi`
* Run the server: `python manage.py runserver`

If there is an error telling you that you need django installed, follow the steps below:
* Install django: `sudo pip install django`
* Install django rest framework: `sudo pip install djangorestframework`
* Install pygments: `sudo pip install pygments`
* Retry running the server: `python manage.py runserver`

See the book listing result by going to the address "http://127.0.0.1:8000/book/"

# Add new functionality to the API
To add a new functionality to the api, follow the steps below.

* Open "Book API Homework/bookapi/book/views.py"  
This file contains the functions. If you want to add a new functionality please add your function here.
* Write your function with the `@csrf_exempt` in the beginning and process the request.
* Open "Book API Homework/bookapi/bookapi/urls.py"
This file contains the urls and their related functions.
* Add your url pattern and link it to your function in views.
* Run server (run `python manage.py runserver` in "(env)/Book API Homework/bookapi")
* Try your newly added url. ("http://127.0.0.1:8000/<your_url>" or via Postman (see below))

# Test the API  
To test the API's GET and POST methods, follow the steps below.  
  
* Download and install Postman from https://www.getpostman.com/apps.  
* Run server (run `python manage.py runserver` in "(env)/Book API Homework/bookapi")
* Open Postman, select your request type (GET, POST, DELETE, etc.), and hit send.

# Runnning existing unit tests  
* Run the environment (`source env/bin/activate`)
* Go into the bookapi folder: `cd bookapi`
* Run the tests: `python manage.py test`

# Adding new unittests  
* Give a name to the url are going to test by adding a name='<chosen-url-name>' attribute to the urls.py file in bookapi folder.  
* Add your test case to the tests.py file in book folder.  
  
CAREFUL: The test database is different from the actual database. Before every test, the test database is cleaned and emptied. If you are adding a GET test, make sure you POST some dummy data beforehand.