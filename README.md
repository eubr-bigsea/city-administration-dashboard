# City Administration Dashboard

City Administration Dashboard is an application that uses Analytics and Visualization techniques on historical data of bus trips of a Public Transport System in order to assist and facilitate planning and monitoring the system.

## Features

- Trips classified as:
    + On time
    + Late
    + Extra
    + Missing
- Route rankings according to:  
    + Number of On time trips
    + Number of Scheduled trips accomplished  
    + Number of extra trips (not scheduled) accomplished  
- Trips are shown in a nice, interactive and easy manner
- Analysis can be filtered by bus, date and route
- Ticketing data analysis is also available per route and per company

## Preprocessing

All features listed above depends on the availability of execution data linked with scheduled data. Obtaining that kind of data requires two steps of data processing. The first one is to identify all perfomed trips on execution data, e.g. GPS data. The second step is match the actual trips with the scheduled trips..

### Finding trips on execution data

In order to split execution data in trips we use an algorithm that measures the similarity of a sequence of GPS coordinates to the shapes of all routes on the system.

### Pairing performed and scheduled trips

This task uses essentially the starting time of both trips. The scheduled trip is paired with the perfomed trip with the closest start time, as long as the difference between them do not exceed the scheduled trip headway. The headway of a scheduled trip is the time diffence, in minutes, betweew its start time and the start time of the next scheduled trip.

# Architecture
<div style="display:table-cell; vertical-align:middle; text-align:center">
  <img src="https://lh6.googleusercontent.com/sYMv9aq_hWDT6UdSwMxt7v-U6Z5l0trE2s8rQg7-tWYGqwmdGrCckCEwTp811pZsSnJ2yuDfeVwjaNQ=w1920-h950-rw" alt="Drawing" align="center"/>
</div>

## Installation/Configuration

### 1 - Launching REST API Server

**Notice:** In this tutorial we assume the usage of Ubuntu 14.04 LTS OS.

Install the required packages:  

```
$ sudo apt-get install python-dev libmysqlclient-dev apt-get install python-virtualenv
```

From inside the folder <tpanalytics-folder-path>/src/restful_api, create a virtual environment:

```
$ virtualenv .venv
```

This command will create a virtual environment inside folder '.venv'.

Then, activate the virtual environment:

```
$ . .venv/bin/activate
$ pip install -U pip
$ pip install -r requirements.txt
```

Now the environment is ready for running REST.  

Create a copy of the file 'config.ini.example' with the name 'config.ini'. This file must be editted with the information of DBMS, among others. There is a sample config.ini file below.

```
----------
config.ini
----------

[Database]
host = put_host_here # DB host/ip. Examples: 143.41.34.145 , bdaddress.com
port = put_port_here # port where DB runs at. Example: 10333
user = put_user_here # DB user name. Example: cganalytics
passwd = put_password_here # DB password. Example: dbpasswd
db_name = put_dbname_here # DB schema. Example: tpanalytics

[REST]
port = put_port_here # port where REST API is running at
secret_key = put_secret_here # secret key to ecrypt session - this key mustn't be public and must only be put here
```

Finally, run the API:

```
$ python run.py
```

### 2 - Launching Observatorium Website Server

Install Apache on your system

```
$ sudo apt-get install apache2
```

Create a symbolic link inside your apache public folder to the website folder (default public folder: /var/www/html):
```
$ sudo ln -s <tpanalytics-folder-path>/artifact/web/ /var/www/html/observatorium
```

## Usage

Execute the website from your browser through localhost:

[http://localhost/observatorium/view](http://localhost/observatorium/view)

