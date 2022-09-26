# Staff Directory Application
Line count: 1322 lines of code

## App Description

This app is an Staff Management System for a company called Media Central.
It contains functionality for a staff directory which lists the details of staff members.

Users can only register themselves on the app if they are a registered staff member. Staff members are created by administrators of the system, admins do this by completing a form on the staff directory pages.

Users of the system can use a connections page to connect with colleagues from a range of different departments. Users can edit and delete the posts that they make and administrators of the app can delete any posts on the connection page.

The structure of this app was based on a tutorial found at:
https://flask.palletsprojects.com/tutorial/

## Prerequist

This code can also be cloned or downloaded from the following github repository: https://github.com/6ec1c80c1dba/staff-directory.

To run this application you will need to follow the directions below to install the neccessary dependencies:

Create and activate your virtualenvironment:

    $ python3 -m venv venv
    $ . venv/bin/activate

Install Dependencies:
$ pip install flask
$ pip install -e .

## Run

To start up the application run the following commands and you will be able to spin up a local server for the application to run on.
.. code-block:: text

    $ flask --app flaskr init-db
    $ flask --app flaskr --debug run

Open http://127.0.0.1:5000/ in a browser.

## Registration Details
To register Sam Park as a user, input the following email address into the register user form.
Username: sampark@mediacentral.com


## Login Details
To login as an administrator for the application, input the following details into the login form.
Username: johnathondove@mediacentral.com
Password: Admin

## Test

::

    $ pip install pytest
    $ python -m pytest
