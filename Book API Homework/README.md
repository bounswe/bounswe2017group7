# Book API
This folder contains an API and an virtualenv.

To copy this branch and work with the API, please follow the steps below:

* Create a folder to copy the branch.
* Clone the repository: `git clone https://github.com/bounswe2017group7.git`
* Go into the folder: `cd bounswe2017group7`
* See all the branches: `git branch -a`
* Checkout to this branch: `git checkout origin/bookapi_booklist`
(The two steps above will not be needed after the pull request is resulted.)
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
