#!/usr/bin/python
import tldrlib
import util
import process_data
from tldrlib import *
from util import *
from process_data import *

print "learning"

# def loadTraining

def processData(numSamples=-1):
    f1 = open('raw_data.txt', 'r')
    f2 = open('processed_data.txt', 'w')
    data = f1.read().split('\n')
    f1.close()

    rawCount = 0
    entryCount = 0
    # for line in data:
