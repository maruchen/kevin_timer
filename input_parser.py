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


class InputParser(object):
    # timestamp is in seconds
    def _get_timestamp_from_now(self, input_time):
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


    def _get_timestamp_from_static_day(self, input_time):
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


    def _get_timestamp_from_static_time(self, input_time):
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


    def _convert_1param_to_timestamp(self, input_time):
        match = re.match(r'\d+[md]', input_time)
        if match is not None:
            absolute_timestamp = self._get_timestamp_from_now(input_time)
            return absolute_timestamp
        
        match = re.match(r'(\d+-)?\d+-\d+', input_time)
        if match is not None:
            absolute_timestamp = self._get_timestamp_from_static_day(input_time)
            return absolute_timestamp

        match = re.match(r'\d+:\d+(:\d+)?', input_time)
        if match is not None:
            absolute_timestamp = self._get_timestamp_from_static_time(input_time)
            return absolute_timestamp

        raise FormatError("value error")


    def _convert_2param_to_timestamp(self, input_day, input_time):
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


    def parse_arguments(self):
        """
        return (absolute_timestamp, thing)
        """
        if len(sys.argv) <= 1:
            raise FormatError("参数太少") 
        # 第一个参数为脚本名，排除
        cmdline = ' '.join(argv[1:]) 
        return self.parse_textline(cmdline)


    def parse_textline(self, cmdline):
        """
        return (absolute_timestamp, thing)
        """
        relative_time_parser = RelativeTimePatternParser()
        pattern_parsers = [relative_time_parser]
        for pattern_parser in pattern_parsers:
            if pattern_parser.match(cmdline):
                return pattern_parser.parse(cmdline)

class PatternParser(object):
    """
    abstract interface
    """
    def match(self, cmdline):
        """
        return: True/False
        """
        raise NotImplementedError 

    def parse(self, cmdline):
        """
        return (absolute_timestamp, thing)
        """
        raise NotImplementedError 


class RelativeTimePatternParser(PatternParser):

    def match(self, cmdline):
        match = re.search(r'\b\d+[md]?\b', cmdline)
        if match:
            return True
        match = re.search(r'\b\d+days?\b', cmdline)
        if match:
            return True

    def parse(self, cmdline):
        # N minutes
        current_timestamp = time.mktime(time.localtime())
        match = re.search(r'\b(\d+)m?\b', cmdline)
        if match:
            input_num = match.group(1)
            due_timestamp = current_timestamp + int(input_num) * 60
            thing = cmdline.replace(match.group(0), " ").strip()
            return (due_timestamp, thing)
        # N days
        current_timestamp = time.mktime(time.localtime())
        match = re.search(r'\b(\d+)(d|day|days)\b', cmdline)
        if match:
            input_num = match.group(1)
            due_timestamp = current_timestamp + int(input_num) * 60 * 60 * 24
            thing = cmdline.replace(match.group(0), " ").strip()
            return (due_timestamp, thing)





