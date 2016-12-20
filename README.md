# City Administration Dashboard

City Administration Dashboard is an application that uses Analytics and Visualization techniques on historical data of bus trips of a Public Transport System in order to assist and facilitate planning and monitoring the system.

## Features

### Rankings

One of the dashboard visualizations is a ranking of the system routes. The intention is to provide a fast and simple way to identify if a route is performing according to the schedule.

<div style="display:table-cell; vertical-align:middle; text-align:center">
  <img src="https://drive.google.com/uc?id=0ByJXvHckLkTdc0dTNEZTNHgxOFU" alt="Drawing" align="center"/>
</div>

On the left ranking, you can see the route punctuality. Route punctuality is basically the percentage of performed trips that were performed without delays. The middle ranking shows the schedule fulfillment, in other words, how many scheduled trips were in fact preformed. On the right ranking, you can see how many performed trips did not have an associated scheduled trip also called extra trips. 

All the data used on each ranking refers to the current day by default but can be changed using the calenda filter highlighted in red.

### Routes daily operation

After looking at information about the system as a whole, you can investigate how was each route operation. The feature called "Escala" displays all performed and scheduled trips on a arch graphic where each trips is shown as an arch.

<div style="display:table-cell; vertical-align:middle; text-align:center">
  <img src="https://drive.google.com/uc?id=0ByJXvHckLkTdVXlOdnQxdkFDTTg" alt="Drawing" align="center"/>
</div>

The x axis represents the hour of the day. By the arch color you will be able to notice if the trip performed on time or late, if the trip did not perform any scheduled trip or if a scheduled trip was not performed at all also called missing trips.

On the top left corner you can filter the visualization by route, date and bus. On the top right corner you can see a operation summary of the current selection. From the left to the right: median duration of a trip, amount of trips performed on time, amount of delayed trips, amount of extra trips, amount of missing trips and the amount of trips performed that day.

The slider on the bottom let you filter all shown trips by their starting time.

## Preprocessing

All features listed above depends on the availability of execution data linked with scheduled data. Obtaining that kind of data requires two steps of data processing. The first one is to identify all performed trips on execution data, e.g. GPS data. The second step is match the actual trips with the scheduled trips..

### Finding trips on execution data

In order to split execution data in trips we use an algorithm that measures the similarity of a sequence of GPS coordinates to the shapes of all routes on the system.

### Pairing performed and scheduled trips

This task uses essentially the starting time of both trips. The scheduled trip is paired with the performed trip with the closest start time, as long as the difference between them do not exceed the scheduled trip headway. The headway of a scheduled trip is the time diffence, in minutes, betweew its start time and the start time of the next scheduled trip.

# Architecture
<div style="display:table-cell; vertical-align:middle; text-align:center">
  <img src="https://drive.google.com/uc?id=0ByJXvHckLkTdbEZCWWl6MF9GcnM" alt="Drawing" align="center"/>
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

