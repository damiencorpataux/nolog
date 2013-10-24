#!/usr/bin/python

import pymongo

def output(data):
    client = pymongo.MongoClient('localhost', 27017)
    collection = client['test']['data']
    for line in data: collection.insert(line)
    
