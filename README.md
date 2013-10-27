nolog
=====

Lightweight pipe-based log harvester for distribution and scaling

# Dependencies
Debian example:
```
sudo apt-get install \
python \
mongodb \
grok

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
*Install dependencies first*

# Data harvest
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

# Name
Because it is developed lurking at logstash, a nice name would be logpystash
