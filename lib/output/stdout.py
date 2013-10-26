#!/usr/bin/python

def output(data):
    for line in data:
        print 'Output: %s' % line
        yield 'Line printed to stdout'
