## Development Setup - For Mac OS X 10

### First-time setup

1) Open a new Terminal window

2) Clone this repository

    git clone <URL OF THIS REPOSITORY>

3) Install Selenium standalone server
    
    cd
    wget http://selenium.googlecode.com/files/selenium-server-standalone-2.31.0.jar

4) Download and install PostgreSQL DB server from http://postgresapp.com/

### Running the scraper

1) Open a new Terminal window

2) Start Selenium standalone server

    cd
    java -jar selenium-server-standalone-2.31.0.jar

3) Open a new Terminal window

4) Navigate to the project root

    cd ~/path/to/your/projects/hermes

5) Start the scraper

    python bin/scraper.py

