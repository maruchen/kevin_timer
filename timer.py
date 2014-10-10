#! /usr/bin/env python
# -*- coding: utf-8 -*-

import os, sys, time
import fileinput
import re
import logging
import argparse
import operator
import math
from input_parser import *


WATCH_FILENAME = "D:/watch.txt"


logging.basicConfig(filename='D:/kevin_timer.log', 
                    filemode='a',
                    level=logging.DEBUG,
                    format='%(levelname)s %(asctime)s %(filename)s:%(lineno)d %(message)s')



#============================ main ===============================
if __name__ == "__main__":
    logging.debug("input:%s", ' '.join(sys.argv))

    #print len(sys.argv)
    #print ' '.join(sys.argv)
    #print os.path.abspath('.') 
    #time.sleep(1000)
    try:
        parser = InputParser()
        (absolute_timestamp, input_todo) = parser.parse_arguments(sys.argv)

    except FormatError as e:
        logging.error("arguments must be in format: time something")
        print "arguments must be in format: time something"
        print "TIPS: examples of time: 5m(5 minutes later), 3d(3 days later), or 11-01(the Nov. 1st in this year), or 2015-1-2, or [2015-]1-2 8:00[:00]"
        exit(1)


    print input_todo + "\t@ " + time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(absolute_timestamp)) + " (" + str(absolute_timestamp) + ")"
    with open(WATCH_FILENAME, 'a') as watch_file:
        watch_file.write(input_todo + "\t@ " + time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(absolute_timestamp)) + " (" + str(absolute_timestamp) + ")\n")


