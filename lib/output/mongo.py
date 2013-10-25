#!/usr/bin/python

import pymongo

def output(data, host='localhost', port=27017, db='nolog', collection='data'):
    client = pymongo.MongoClient('localhost', 27017)
    collection = client[db][collection]
    return [collection.insert(line) for line in data]
