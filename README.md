# Rick's Wine Journal

This project was developed for the "catalog project" in the Udacity Full Stack Web Development Course.  It creates a
crowd sourced journal of wine and wine tastings

https://ourwinejournal.com

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

## API Endpoints
All returns are json objects

`/users/api/v1/login/` - takes a json object with username and password - returns the user object
`/users/api/v1/<int:user_id>/` - returns a user object
`/users/api/v1/logout/` - logs out & deletes the session

`/categories/api/v1/categories/` - returns an object of all category objects
`/categories/api/v1/<int:category_id>/` - returns a category object

`/comments/api/v1/comments/` - returns an object of all comment objects
`/comments/api/v1/<int:comment_id>/` - returns a comment object

`/regions/api/v1/regions/` - returns an object of all region objects
`/regions/api/v1/<int:region_id>/` - returns a region object

`/tasting-notes/api/v1/tasting-notes/` - returns an object of all tasting note objects
`/tasting-notes/api/v1/<int:tnote_id>/` - returns a tasting note object

`/wines/api/v1/wines/` - returns an object of all wine objects
`/wines/api/v1/<int:wine_id>/` - returns a wine object

## Future Development

1. Add sms notifications of updates
2. Add WikiPedia API for region & category desriptions
3. Add non-social login & registration
4. Add email both for notifications & password recovery
5  Add WYSIWYG type editor for descriptions & notes (TinyMCE?)
6. Add search by rating
7. Add sort by price
8. Add links in wines to categories and regions
9. Add Snooth API information for wines & wineries
10. Move all text that should be customizeable into a settings configuration (make it portable)
11. Add scrst designations to images, resize images for smaller screens
12. Add _author's page_ to display posts by user - make name clickable


