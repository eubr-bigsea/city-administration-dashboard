# City Administration Dashboard

City Administration Dashboard is an application that uses Analytics and Visualization techniques on historical data of bus trips of a Public Transport System in order to assist e facilitate planning and monitoring the system.

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

