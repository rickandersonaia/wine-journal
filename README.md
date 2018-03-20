# Rick's Wine Journal

This project was developed for the "catalog project" in the Udacity Full Stack Web Development Course.  It creates a
crowd sourced journal of wine and wine tastings

## Project description

## Development server

1. Download a copy of the Vagrant file from https://github.com/udacity/fullstack-nanodegree-vm
2. Add the following lines of code after line 30

    `pip3 install flask-assets webassets pytest pytest-flask pytest-cov flake8 scss
     pip3 install psycopg2 flask-wtf wtforms-components flask-debugtoolbar flask-login
     pip3 install `

3. In the terminal window run `vagrant up --provision`
4. In the same terminal window run `vagrant ssh`
5. Then `cd /vagrant`
6. clone this librarary into the /vagrant directory
7. Then `cd /wine-journal`
3. In the terminal window run `python3 run.py`
4. Navigate to `http://localhost:500/`. The app will automatically reload if you change any of the source files.

## Code scaffolding

All of the necessary dependencies should already be installed, however the requirements.txt file
contains all of the dependencies of the project.  Running `pip3` will install them

## Build

JavaScript, SCSS and images are compiled, compressed and minimized upon save. The build artifacts will be stored in the `static/` directory.

## Custom CLI

From the root directory run `winejournal` to see the commands available

## Running unit tests

From the root directory run `winejournal test` to run the unit tests.  This library uses pytest.
Run `winejournal cov` for the unit test coverage report

## Running code quality tests

From the root directory run `winejournal flake8` to run the code quality tests.

## Running end-to-end tests

Nothing yet
