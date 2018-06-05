# Log Analysis Project

This script produces the following 3 reports based on the "Udacity News DB":

1. Top 3 most popular articles
2. Authors ordered by number of their article views
3. HTTP error report, showing days with more than 1% errors

It is assumed that the "Udacity News DB" is already installed and running in a PostgreSQL DB.

The script creates the connection to the PostgreSQL DB and runs the required SQL queries outputting the report to the terminal display.

For some of the reports the views are created to support the calculation of the reports. These views are created and cleaned up within the script.

## Example output

The reported output is shown as follows:


|      Top 3 most popular articles      |   Views   |
----------------------------------------|-------------|
|   Candidate is jerk, alleges rival    |  342102   |
|   Bears love berries, alleges bear    |  256365   |
|   Bad things gone, say good people    |  171762   |


|                Author                 |   Views   |
----------------------------------------|-------------|
|   Ursula La Multa                     |   512805  |
|   Rudolf von Treppenwitz              |   427781  |
|   Anonymous Contributor               |   171762  |
|   Markoff Chaney                      |   85387   |


|            Date              |   Percent Errors   |
-------------------------------|----------------------|
|         2016-07-17           |        2.26        |



## How to use
The server is written in Python 3.6.5, so Python 3 shall be downloaded and used to run the file log_analysis.py.
Python 2 can be used but the PostgreSQL library will be required (see troubleshooting guide)

1. Clone the directory
2. Navigate to the directory cd repository_name
3. If needed download Python 3 (version 3.6.5 is recommended)
4. IDLE: Open IDLE
3. To run the program with the command `python3 log_analysis.py` or `python2 log_analysis.py`
5. In the menu bar click on Run -> Run Module or press F5 on your keyboard

The PostgreSQL database can be downloaded and installed from here:
https://www.postgresql.org/download/ 
The application has been tested with version 9.5.12.

## Troubleshooting
If the error "no module named psycopg2" is received, it is likely Python 2.x is being run.  Please upgrade to Python 3.6.5 here:
https://www.python.org/downloads/ 

Alternatively download the psycopg2 library:

1. From the directory containing the script, install the dependencies:
`sudo apt-get build-dep python-psycopg2`

2. Then install the library:
`pip install psycopg2` 

The application has been tested with Pyscopg 2.7.4.