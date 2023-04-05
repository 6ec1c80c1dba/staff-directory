# Staff Directory Application
Line count: 1500 lines of code

## App Description

This app is an Staff Management System for a company called Media Central.
It contains functionality for a staff directory which lists the details of staff members.

Users can only register themselves on the app if they are a registered staff member. Staff members are created by administrators of the system, admins do this by completing a form on the staff directory pages.

Users of the system can use a connections page to connect with colleagues from a range of different departments. Users can edit and delete the posts that they make and administrators of the app can delete any posts on the connection page.

The source code for this application can also be cloned or downloaded from the following github repository: https://github.com/6ec1c80c1dba/staff-directory.

The structure of this app was based on a tutorial found at:
https://flask.palletsprojects.com/tutorial/

## App Security Configuration

Flask Talisman is an extension which has been applied to the staff directory application to configure application security headers with best practice default values.

As outlined within the [PYPI Documentation](https://pypi.org/project/talisman/) the following headers and relative valueshave been set:
force_https, default True, forces all non-debug connects to https.
force_https_permanent, default False, uses 301 instead of 302 for https redirects.
frame_options, default SAMEORIGIN, can be SAMEORIGIN, DENY, or ALLOWFROM.
frame_options_allow_from, default None, a string indicating the domains that arrow allowed to embed the site via iframe.
strict_transport_security, default True, whether to send HSTS headers.
strict_transport_security_max_age, default ONE_YEAR_IN_SECS, length of time the browser will respect the HSTS header.
strict_transport_security_include_subdomains, default True, whether subdomains should also use HSTS.
content_security_policy, default default-src: 'self', see the section below.
session_cookie_secure, default True, set the session cookie to secure, preventing it from being sent over plain http.
session_cookie_http_only, default True, set the session cookie to httponly, preventing it from being read by JavaScript.

## Prerequist

To run this application you will need to follow the directions below to install the neccessary dependencies:

Create and activate your virtualenvironment:

    $ python3 -m venv venv
    $ . venv/bin/activate

The use of a virtual environment enables end-users to install the neccessary dependencies required for the staff directory project without version or type conflicts which can occur when attempting run libraries already installed on developers systems but with a newer version than that required for the application.

Install Dependencies:
$ pip install flask pyopenssl
$ pip install flask-talisman flask-marshmallow flask-wtf
$ pip install -e .

## Run

To start up the application run the following commands and you will be able to spin up a local development server for the application to run on.

To initialise the database, run:
    $ flask --app flaskr init-db
To run the application with HTTP, run: 
    $ flask --app flaskr --debug run
    Open http://127.0.0.1:5000/ in a browser.
To run the application on HTTPS, run:
    $ flask --app flaskr --debug run --cert adhoc
    Open https://127.0.0.1:5000/ in a browser.

Open http://127.0.0.1:5000/ in a browser.

## Registration Details
To register Sam Park as a user, input the following email address into the register user form and specify a password of your choice.
Username: sampark@mediacentral.com


## Login Details
To login as an administrator for the application, input the following details into the login form.
Username: johnathondove@mediacentral.com
Password: 8bnewLsbZv

## Test

Install the test dependency:
    $ pip install pytest

Run the unit tests for the application:
    $ python -m pytest
