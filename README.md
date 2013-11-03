nolog
=====

Lightweight pipe-based log harvester for distribution and scaling

# Dependencies
Debian example:
```
sudo apt-get install \
python \
mongodb \
groka

sudo apt-get install pip
pip install pymongo
```

# Install
Debian example (again):
```
cd ~
git clone git@github.com:damiencorpataux/nolog.git
cd nolog.git
```

# Data harvest
Being a simple but powerful pipe, nolog allows you to combine inputs, filters and output to fit your data collecting needs.

### Data pull
In this situation, the monitor node(s) pull data from monitored node(s).

Edit ```conf/sample.py````and update the plan to your needs.
```
TODO: Comment conf/sample.py well and put it here as a gist
```

Run the harvester.
```
cd ~/nolog
python processing.py
```

Have a look at the harvested data using mongodb command line interface.
```
damien@fast:~$ mongo
MongoDB shell version: 2.0.6
connecting to: test
> use nolog
switched to db nolog
> db.data.count()
27640
> db.data.find()
{ "_id" : ObjectId("526be2fc31d4544d9d415b67"), "timestamp" : 1382799951, "message" : "printing/print_cups.c:487(cups_async_callback)\nfailed to retrieve printer list: NT_STATUS_UNSUCCESSFUL", "time" : "2013/10/26 17:05:51.919165" }
{ "_id" : ObjectId("526be37b31d4544dd8d8ea67"), "timestamp" : 1382801513, "message" : "printing/print_cups.c:487(cups_async_callback)\nfailed to retrieve printer list: NT_STATUS_UNSUCCESSFUL", "time" : "2013/10/26 17:31:53.079103" }
{ "_id" : ObjectId("526be37b31d4544dd8d8ea68"), "timestamp" : 1382802293, "message" : "printing/print_cups.c:110(cups_connect)\nUnable to connect to CUPS server localhost:631 - Connection refused", "time" : "2013/10/26 17:44:53.609363" }
{ "_id" : ObjectId("526be37b31d4544dd8d8ea69"), "timestamp" : 1382802293, "message" : "printing/print_cups.c:487(cups_async_callback)\nfailed to retrieve printer list: NT_STATUS_UNSUCCESSFUL", "time" : "2013/10/26 17:44:53.617070" }
[...]
has more
```

### Data pull
In this situation, the monitored node(s) push data to the monitoring node(s). At this stage of development, some inputs and outputs have to be written.

The idea is to combine input/outputs like so:
```
# This plan filters data on monitored node and inserts the result directly
# in the monitoring node mongo collection
plan = {
    'input': [{
        'module': 'shell', 'options': { command: 'since /var/log/syslog' }
    }],
    'filter': [{
        'module': 'syslog'
    }],
    'output': [{
        'module': 'mongo', 'options': { 'host': 'monitor.local' }
    }]
}
```

Or if you want your monitored nodes to process as little as possible:
```
# This plan is executed (cron) on the monited node and pushes raw loglines
# to the moniting node by appending data to a file 
plan = {
    'input': [{
        'module': 'shell', 'options': { command: 'since /var/log/syslog' }
    }],
    'filter': [
        # no data filtering
    ],
    'output': [{
        # This input should: append data to a file on monitor.local
        # (creating the file if necessary)
        'module': 'sshappend', 'options': { 'host': 'monitor.local', 'file': '/tmp/nodename/syslog }
    }]
}

# This plan is executed (cron) on the moniting node, it parses pushed loglines
# and outputs the data to mongo collection
plan = {
    'input': [{
        'module': 'shell', 'options': { command: 'cat /tmp/nodename/syslog' }
    }],
    'filter': [
        'module': 'syslog'
    ],
    'output': [{
        'module': 'mongo'
        # The processed loglines are stripped from file upon completion
        'module': 'stripline', 'options': { 'file': '/tmp/nodename/syslog }
    }]
}
```

# Name
Because it is developed lurking at logstash, a nice name would be logpystash (as in pistache nuts).

Also, this software could be named pype, because it is in fact a *python pipe* engine.
