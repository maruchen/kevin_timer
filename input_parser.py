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


DEFAULT_TIME_OF_DAY = "8:00"

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
        absolute_time_whth_date__parser = AbsoluteTimeWithDatePatternParser()
        absolute_time_whthout_date__parser = AbsoluteTimeWithoutDatePatternParser()
        pattern_parsers = [
                            absolute_time_whth_date__parser,
                            absolute_time_whthout_date__parser,
                            relative_time_parser
                          ] # 顺序很重要
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
        return False

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

        raise FormatError("传入不符合格式的参数") 


class AbsoluteTimeWithDatePatternParser(PatternParser):

    def match(self, cmdline):
        match = re.search(r'\b\d+-\d+(-\d+)?\b', cmdline)
        if match:
            return True

    def parse(self, cmdline):

        # 找日期对应的standard_date, date_timestamp
        match = re.search(r'\b(\d+-\d+-\d+)\b', cmdline)
        if match:
            standard_date = match.group(1)
            date_timestamp = time.mktime(time.strptime(standard_date, "%Y-%m-%d"))
            cmdline = cmdline.replace(match.group(0), " ").strip()
        else:
            match = re.search(r'\b(\d+-\d+)\b', cmdline)
            if match:
                year = time.localtime().tm_year
                standard_date = str(year) + "-" + match.group(1)
                date_timestamp = time.mktime(time.strptime(standard_date, "%Y-%m-%d"))
                cmdline = cmdline.replace(match.group(0), " ").strip()
            else:
                raise FormatError("传入不符合格式的参数") 

        # 00:00
        match = re.search(r'\b(\d+:\d+)\b', cmdline)
        if match:
            standard_time_str = standard_date + " " + match.group(1)
            due_timestamp = time.mktime(time.strptime(standard_time_str, "%Y-%m-%d %H:%M"))
            thing = cmdline.replace(match.group(0), " ").strip()
            return (due_timestamp, thing)

        # 00am
        match = re.search(r'\b(\d+)am\b', cmdline)
        if match:
            standard_time_str = standard_date + " " + match.group(1) + ":00"
            due_timestamp = time.mktime(time.strptime(standard_time_str, "%Y-%m-%d %H:%M"))
            thing = cmdline.replace(match.group(0), " ").strip()
            return (due_timestamp, thing)

        # 00pm
        match = re.search(r'\b(\d+)pm\b', cmdline)
        if match:
            standard_time_str = standard_date + " " + str(int(match.group(1)) + 12) + ":00"
            due_timestamp = time.mktime(time.strptime(standard_time_str, "%Y-%m-%d %H:%M"))
            thing = cmdline.replace(match.group(0), " ").strip()
            return (due_timestamp, thing)

        # 只指定日期，没有指定时间
        else:
            standard_time_str = standard_date + " " + DEFAULT_TIME_OF_DAY
            due_timestamp = time.mktime(time.strptime(standard_time_str, "%Y-%m-%d %H:%M"))
            thing = cmdline.strip()
            return (due_timestamp, thing)


class AbsoluteTimeWithoutDatePatternParser(PatternParser):

    def match(self, cmdline):
        match = re.search(r'\b(\d+:\d+)\b', cmdline)
        if match:
            return True
        
        match = re.search(r'\b(\d+)am\b', cmdline)
        if match:
            return True

        match = re.search(r'\b(\d+)pm\b', cmdline)
        if match:
            return True

        return False

    def parse(self, cmdline):
        year = time.localtime().tm_year
        month = time.localtime().tm_mon
        day = time.localtime().tm_mday
        standard_date = str(year) + "-" + str(month) + "-" + str(day)

        # 00:00
        match = re.search(r'\b(\d+:\d+)\b', cmdline)
        if match:
            standard_time_str = standard_date + " " + match.group(1)
            due_timestamp = time.mktime(time.strptime(standard_time_str, "%Y-%m-%d %H:%M"))
            if due_timestamp < time.time():
                due_timestamp += 24 * 60 * 60  # 当天已过期，算到第二天
            thing = cmdline.replace(match.group(0), " ").strip()
            return (due_timestamp, thing)

        # 00am
        match = re.search(r'\b(\d+)am\b', cmdline)
        if match:
            standard_time_str = standard_date + " " + match.group(1) + ":00"
            due_timestamp = time.mktime(time.strptime(standard_time_str, "%Y-%m-%d %H:%M"))
            if due_timestamp < time.time():
                due_timestamp += 24 * 60 * 60
            thing = cmdline.replace(match.group(0), " ").strip()
            return (due_timestamp, thing)

        # 00pm
        match = re.search(r'\b(\d+)pm\b', cmdline)
        if match:
            standard_time_str = standard_date + " " + str(int(match.group(1)) + 12) + ":00"
            due_timestamp = time.mktime(time.strptime(standard_time_str, "%Y-%m-%d %H:%M"))
            thing = cmdline.replace(match.group(0), " ").strip()
            if due_timestamp < time.time():
                due_timestamp += 24 * 60 * 60
            return (due_timestamp, thing)

        else:
            raise FormatError("传入不符合格式的参数") 



