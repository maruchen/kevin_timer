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
from store import *




logging.basicConfig(filename='D:/kevin_timer.log', 
                    filemode='a',
                    level=logging.DEBUG,
                    format='%(levelname)s %(asctime)s %(filename)s:%(lineno)d %(message)s')



#============================ main ===============================
if __name__ == "__main__":
    logging.debug("input:%s", ' '.join(sys.argv))

    try:
        parser = InputParser()
        (absolute_timestamp, input_todo) = parser.parse_arguments()

    except FormatError as e:
        logging.error("arguments must be in format: time something")
        print "arguments must be in format: time something"
        print "TIPS: examples of time: 5m(5 minutes later), 3d(3 days later), or 11-01(the Nov. 1st in this year), or 2015-1-2, or [2015-]1-2 8:00[:00]"
        time.sleep(10)
        exit(1)

    except Exception as e:
        logging.error("unknown exception:%s", str(e))
        print str(e)
        time.sleep(10)
        exit(1)

    print "done"
    print input_todo + "\t@ " + time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(absolute_timestamp)) + " (" + str(absolute_timestamp) + ")"
    logging.debug("parse ok:%s", input_todo + "\t@ " + time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(absolute_timestamp)) + " (" + str(absolute_timestamp) + ")")
    time.sleep(1)


    store = Store()
    if input_todo == "":
        input_todo = "@" 
    task = Task(None, input_todo, absolute_timestamp, False)
    store.add_task(task)


