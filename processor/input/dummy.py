#!/usr/bin/python

""" This input returns an arbitrary log line or a default dummy """

def process(data=None, count=10, line=None):
    for i in range(count):
        yield line or '2014/01/01 00:00:00+0000 This is a dummy log ling'
