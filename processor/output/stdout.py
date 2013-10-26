#!/usr/bin/python

def process(data):
    for line in data:
        print 'Output: %s' % line
        yield 'Line printed to stdout'
