# Rick's Wine Journal

This project was developed for the "catalog project" in the Udacity Full Stack Web Development Course.  It creates a
crowd sourced journal of wine and wine tastings

## Project description

## Development server

1. Download a copy of the Vagrant file from https://github.com/udacity/fullstack-nanodegree-vm
2. Add the following lines of code after line 30

    `pip3 install flask-assets webassets pytest pytest-flask pytest-cov flake8 scss
     pip3 install psycopg2 flask-debugtoolbar flask-login flask-dance boto3
     pip3 install WTForms-Alchemy flask-wtf wtforms-components flask-uploads`

3. In the terminal window run `vagrant up --provision`
4. In the same terminal window run `vagrant ssh`
5. Then `cd /vagrant`
6. clone this librarary into the /vagrant directory
7. Then `cd /wine-journal`
8. In the terminal window run `pip install -r requirements.txt --no-index`
3. In the terminal window run `python3 run.py`
4. Navigate to `http://localhost:500/`. The app will automatically reload if you change any of the source files.

## Code scaffolding

All of the necessary dependencies should already be installed, however the requirements.txt file
contains all of the dependencies of the project.  Running `pip install -r requirements.txt --no-index` will install them

## Custom CLI

From the root directory run `winejournal` to see the commands available

## Create and Initialize the Database

From the root directory run `winejournal db` to see the commands available.  The `init` command will build a new database, setup the tables and create a default admin user.
Run `winejournal db init` to initialize the database, including adding a default user
Run `winejournal db reset` to delete and reinitialize the database
Run `winejournal db seed` to add the default user to the existing database
The `--with-testdb` flad will create a database with the data base uri appended by _test

## Setup Social Media Login

This application relies on social media login using Flask Dance.  You will need to create apps and credentials at google, twitter and facebook.
See the documentation at https://flask-dance.readthedocs.io/en/latest/.  The settings can be found in `wine-journal/config/settings.py`

## Setup Amazon AWS S3

This application stores and serves images from Amazon S3.  You will need to create a group, user and bucket in order for this feature to work.
See the documentation at http://boto3.readthedocs.io/en/latest/guide/quickstart.html for instructions.

## Setup the initial Admin User

There are many functions in this application that are only available to users with the 'admin' role.
1. To create your first admin user sign in with your favorite social media application.
2. Go to your account on the menu
3. Change the user role to 'admin'
4. Open `wine-journal/config/setting` in a code editor
5. Change the `INITIAL_ADMIN_SETUP = False` to "True"
6. This will hide all admin role protected settings and urls from users with the regular "member" role.

## Build

JavaScript, SCSS and images are compiled, compressed and minimized upon save. The build artifacts will be stored in the `static/` directory.

## Running unit tests

From the root directory run `winejournal test` to run the unit tests.  This library uses pytest.
Run `winejournal cov` for the unit test coverage report
Run `winejournal flake8` for code standards check.

## Running code quality tests

From the root directory run `winejournal flake8` to run the code quality tests.

## Running end-to-end tests

Nothing yet
