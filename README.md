# Crypto:

Author: Naama Ditur

A Web Application for getting the latest crypto currency quotes and give the information like the whole metrics (pairs) in the system, 
the last X hours prices of a given metric and the calculated rank of each metric (pair) in the last X hours.

The web application is a FastApi web framework.
The application poll the data from the following source https://docs.cryptowat.ch/rest-api/.

For triggering the polling of the prices each 1 minutes, you should call (once) the /poll API (see below).
In the future we might add a REST API for getting the prices and saving hem in the DB and a lambda (for example) 
can be scheduled to call that API each X minutes.


## Build:

`docker build -t crypto .`

## Run:
For running the application in a docker and listen to port 5000
`docker run -p 5000:80 crypto`


## Rest Api:

For triggering the polling of the prices each 1 minute:
~~~
curl -X POST "http://localhost:5000/poll"
~~~

---
For gettomg the entire pairs (metrics) in the database:
~~~
curl "http://localhost:5000/pairs"
~~~
#####Response example:
["nctbtc","xaurbtc","wildweth","btgeur","shftusd"]

---
For getting the last prices of the given metric (pair) in the last X hours:
~~~
curl "http://localhost:5000/get_last_metric_prices?metric=btcusd&last_hours=5"
~~~
If non last_hours is given, the default is 24 hours
#####Response example:
[["2022-07-16T22:56:18",21254.73,"btcusd","okcoin"],["2022-07-16T22:56:18",21000.0,"btcusd","zonda"],...]

---

For getting the ranks of whole the pairs (metrics) in last X hours:
~~~
curl "http://localhost:5000/get_ranks?last_hours=5"
~~~
If non last_hours is given, the default is 24 hours
#####Response example:
[["baxbtc",0.9995502248875562],["bcdeth",0.9997001499250375],["edgbtc",0.9998500749625188],["locusdt",1.0],...]


### Before running in the first time:
Before running the application for the first time you should create a DB and fill the paramters
in DBUtil.py: host, user, password, database and port.
#####ToDo: Get the DB parameters from AWS SECRET


#### ToDos:

1. The prices per metric (pair) is presented for all the markets. we can add a parameter for filtering by specific market.
2. The rank is calculated according the STD which is calculated per metric (pair) regardless of the market. We can calculate the rank per pair + market.

#### Answering the questions:
#####Scalability:
1. FastAPi is quite scalable. 
2. For tracking many metrics we can add list of metrics to the Rest API in the request body.
3. For sampling the data more frequently we can give the interval as a parameter or giving the option to schedule the polling outside this scope (in a lambda for example) as I mentioned above.
4. For serving many users in the dashboard we can cache results and serve from the cache.

#####Testing:
This application was manually tested. We should add automation for testing the system:
- Unit test - to test each model in the system
- Integration test to test the system with a mocked data
- System tests to test the system E2E

#####Feature request:
When getting the prices and saving them in the DB, we can calculate the average for the last 1 hour per metric.
Then we can identify the metric which its price exceeds the average by X3. 
We can add to the system an API for subscribing for such alerting. 
The API can enable for subscribing for all metrics or for specific metric 
and give an e-mail address or phone number for getting the alerts by a mail or sms (for example).
Then we'll send the alert to all subscriber, using AWS SNS (for example).
