#! /usr/bin/env python  
# -*- coding: utf-8 -*-

import os, sys, time
import fileinput
import re
import logging
import argparse
import operator
import math

#TODO 单测


DEFAULT_TIME_OF_DAY = "10:00:00"

class FormatError(Exception):
    pass


# timestamp is in seconds
def get_timestamp_from_now(input_time):
    match = re.match(r'(\d+)(\D+)', input_time)
    if match is not None:
        multiple = 60
        if match.group(2) == 'm':
            multiple = 60
        elif match.group(2) == 'd':
            multiple = 60 * 24
        absolute_timestamp = time.mktime(time.localtime()) + int(match.group(1)) * multiple
        return absolute_timestamp

    raise FormatError("value error")


def get_timestamp_from_static_day(input_time):
    standard_time_string = "";
    match = re.match(r'\d+-\d+-\d+', input_time)
    if match is not None:
        standard_time_string = input_time + " " + DEFAULT_TIME_OF_DAY

    else:
        match = re.match(r'\d+-\d+', input_time)  # no year
        if match is not None:
            year = time.localtime().tm_year
            standard_time_string = str(year) + "-" + input_time + " " + DEFAULT_TIME_OF_DAY

        else:
            raise FormatError("value error")

    absolute_timestamp = time.mktime(time.strptime(standard_time_string, "%Y-%m-%d %H:%M:%S")) 
    return absolute_timestamp


def get_timestamp_from_static_time(input_time):
    standard_time_string = time.strftime("%Y-%m-%d", time.localtime())       
    match = re.match(r'\d+:\d+:\d+', input_time)
    if match is not None:
        standard_time_string = standard_time_string + " " + input_time

    else:
        match = re.match(r'\d+:\d+', input_time)  # no seconds
        if match is not None:
            standard_time_string = standard_time_string + " " + input_time + ":00"

        else:
            raise FormatError("value error")

    absolute_timestamp = time.mktime(time.strptime(standard_time_string, "%Y-%m-%d %H:%M:%S")) 
    return absolute_timestamp


def convert_1param_to_timestamp(input_time):
    match = re.match(r'\d+[md]', input_time)
    if match is not None:
        absolute_timestamp = get_timestamp_from_now(input_time)
        return absolute_timestamp
    
    match = re.match(r'(\d+-)?\d+-\d+', input_time)
    if match is not None:
        absolute_timestamp = get_timestamp_from_static_day(input_time)
        return absolute_timestamp

    match = re.match(r'\d+:\d+(:\d+)?', input_time)
    if match is not None:
        absolute_timestamp = get_timestamp_from_static_time(input_time)
        return absolute_timestamp

    raise FormatError("value error")


def convert_2param_to_timestamp(input_day, input_time):
    standard_time_string = "";
    match = re.match(r'\d+-\d+-\d+', input_day)
    if match is not None:
        standard_time_string = input_day
    else:
        match = re.match(r'\d+-\d+', input_day)  # no year
        if match is not None:
            year = time.localtime().tm_year
            standard_time_string = str(year) + "-" + input_day
        else:
            raise FormatError("input_day error")

    match = re.match(r'\d+:\d+:\d+', input_time)
    if match is not None:
        standard_time_string = standard_time_string + " " + input_time
    else:
        match = re.match(r'\d+:\d+', input_time)  # no seconds
        if match is not None:
            standard_time_string = standard_time_string + " " + input_time + ":00"
        else:
            raise FormatError("input_time error")

    absolute_timestamp = time.mktime(time.strptime(standard_time_string, "%Y-%m-%d %H:%M:%S")) 
    return absolute_timestamp


def parse_arguments(argv):
    if len(argv) < 3:
        raise FormatError("input_time error")

    # decide time is first argument or first two arguments
    match = re.match(r'(\d+-)?\d+-\d+ \d+:\d+(:\d+)?', argv[1] + " " + argv[2])
    if match:
        absolute_timestamp = convert_2param_to_timestamp(argv[1], argv[2])
        input_todo = ' '.join(argv[3:])
    else:
        absolute_timestamp = convert_1param_to_timestamp(argv[1])
        input_todo = ' '.join(argv[2:])

    return (absolute_timestamp, input_todo)






