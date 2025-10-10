# Flask simple realtime dashboard

## How to run

### Create the environment
Create the python environment:
    
    $ python -m venv .venv

Start the environment, example commando for linux bash systems:

    $ source .venv/bin/activate

### Install dependencies

    $ pip install -r requirements.txt

### Setup variables

The project read the SECRET_KEY and SQLALCHEMY_DATABASE_URI environment variables
to configure the secret key and the URI for the Database.
You need to set up a SECRET_KEY to start the app

You can configure the variables with the .env file, you can use the example file:

    $ cp .env.example .env


### Start web server

First setup the db:

    $ flask db init
    $ flask db migrate -m "first migrate"
    $ flask db upgrade

And now you can start the web server:

    $ flask run