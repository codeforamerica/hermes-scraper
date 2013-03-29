## Development Setup - For Mac OS X 10

### First-time setup

1) Open a new Terminal window

2) Clone this repository

    git clone <URL OF THIS REPOSITORY>

3) Install Selenium standalone server (this will take a little less than a minute)
    
    curl http://selenium.googlecode.com/files/selenium-server-standalone-2.31.0.jar > ~/selenium-server-standalone-2.31.0.jar

4) Download and install PostgreSQL DB server from http://postgresapp.com/. Make sure it is running.

5) Return to the Terminal window if you still have it open. If not, open a new one.

6) Create the PostgreSQL user (aka role) and database

    createuser hermes_scraper
    createdb hermes -O hermes_scraper

7) Navigate to the project root

    cd hermes-scraper

8) Initialize the database schema

    python bin/db_init.py

9) Install project dependencies

    pip -r requirements.txt

10) Install Firefox (required by the scraper to emulate a human user searching for cases)

### Running the scraper (IMPORTANT! Please run during off-hours in Kentucky)

1) Open a new Terminal window

2) Start Selenium standalone server

    cd
    java -jar selenium-server-standalone-2.31.0.jar

3) Open a new Terminal window

4) Navigate to the project root

    cd hermes-scraper

5) Start the scraper

    python bin/scraper.py

