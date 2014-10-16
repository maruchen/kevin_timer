#! /usr/bin/env python  
# -*- coding: utf-8 -*-

from input_parser import InputParser
import unittest
import os, sys, time
import fileinput
import re
import logging
import argparse
import operator
import math

        #self.assertEqual(1, 1)
        #self.assertTrue(True)

class TestInputeParser(unittest.TestCase):

    def setUp(self):   # 构建
        pass

    def test_relative_time(self):  # test开头的方法会被自动调用
        test_cases = [
                        # N minutes
                        (
                            "0m abc",
                            (time.mktime(time.localtime()) + 60 * 0, "abc")
                        ),
                        (
                            "5m 中文",
                            (time.mktime(time.localtime()) + 60 * 5, "中文")
                        ),
                        (
                            "5 onlynum中文",
                            (time.mktime(time.localtime()) + 60 * 5, "onlynum中文")
                        ),
                        (
                            "5",  # 匿名事件
                            (time.mktime(time.localtime()) + 60 * 5, "")
                        ),
                        (
                            "abc 99m", # 顺序
                            (time.mktime(time.localtime()) + 60 * 99, "abc")
                        ),
                        (
                            "中文 空格 99m",
                            (time.mktime(time.localtime()) + 60 * 99, "中文 空格")
                        ),
                        # N days
                        (
                            "0d abc space",
                            (time.mktime(time.localtime()) + 24 * 60 * 60 * 0, "abc space")
                        ),
                        (
                            "9d abc",
                            (time.mktime(time.localtime()) + 24 * 60 * 60 * 9, "abc")
                        ),
                        (
                            "100d abc",
                            (time.mktime(time.localtime()) + 24 * 60 * 60 * 100, "abc")
                        ),
                        (
                            "100day abc",
                            (time.mktime(time.localtime()) + 24 * 60 * 60 * 100, "abc")
                        ),
                        (
                            "100days abc",
                            (time.mktime(time.localtime()) + 24 * 60 * 60 * 100, "abc")
                        ),
                        (
                            "abc 100day",
                            (time.mktime(time.localtime()) + 24 * 60 * 60 * 100, "abc")
                        ),
                     ]
        parser = InputParser()
        for test_case in test_cases:
            (due_timestamp, thing) = parser.parse_textline(test_case[0])
            self.assertEqual(test_case[1], (due_timestamp, thing))


    def test_absolute_time_with_date(self):
        year = time.localtime().tm_year
        month = time.localtime().tm_month
        day = time.localtime().tm_day
        today_timestamp = time.mktime(time.strptime(year + month + day, "%Y%m%d"))  
        test_cases = [
                        (
                            "2014-11-1 abc",   # 默认是早上8点提醒
                            (1414800000.0, "abc")
                        ),
                        (
                            "11-1 abc",
                            (1414800000.0, "abc")
                        ),
                        (
                            "abc 11-1",
                            (1414800000.0, "abc")
                        ),
                        (
                            "2014-11-1 16:30 中文",   
                            (1414830600.0, "中文")
                        ),
                        (
                            "11-1 16:30 中文",   
                            (1414830600.0, "中文")
                        ),
                        (
                            "中文 11-1 11pm",   
                            (1414854000.0, "中文")
                        ),
                        (
                            "中文 11-1 23am",   
                            (1414854000.0, "中文")
                        ),
                        (
                            "中文 11-1 2am",   
                            (1414778400.0, "中文")
                        )
                     ]
        parser = InputParser()
        for test_case in test_cases:
            (due_timestamp, thing) = parser.parse_textline(test_case[0])
            self.assertEqual(test_case[1], (due_timestamp, thing))

    def test_absolute_time_without_date(self):
        year = time.localtime().tm_year
        month = time.localtime().tm_month
        day = time.localtime().tm_day
        today_timestamp = time.mktime(time.strptime(str(year) + str(month) + str(day), "%Y%m%d"))  
        tomorrow_timestamp = time.mktime(time.strptime(str(year) + str(month) + str(day + 1), "%Y%m%d"))  

        # 如果现在过了2点，那么指的是第二天的2点，否则指的是今天的2点
        if time.localtime().tm_hour > 2 or (time.localtime().tm_hour == 2 and time.localtime().tm_minute > 0):
            timestamp_for_2 = tomorrow_timestamp
        else:
            timestamp_for_2 = today_timestamp
        # 如果现在过了23点，那么指的是第二天的23点，否则指的是今天的23点
        if time.localtime().tm_hour > 23 or (time.localtime().tm_hour == 23 and time.localtime().tm_minute > 0):
            timestamp_for_23 = tomorrow_timestamp
        else:
            timestamp_for_23 = today_timestamp


        test_cases= [
                        (
                            "23:00 中文",   
                            (timestamp_for_23+23*60*60, "中文")
                        ),
                        (
                            "23am 中文",   
                            (timestamp_for_23+23*60*60, "中文")
                        ),
                        (
                            "11pm 中文",   
                            (timestamp_for_23+23*60*60, "中文")
                        ),
                        (
                            "2am 中文",   
                            (timestamp_for_2+2*60*60, "中文")
                        ),
                        (
                            "中文abc 2:00 中文",   
                            (timestamp_for_2+2*60*60, "中文abc中文")
                        ),
                     ]
        parser = InputParser()
        for test_case in test_cases:
            (due_timestamp, thing) = parser.parse_textline(test_case[0])
            self.assertEqual(test_case[1], (due_timestamp, thing))

if __name__ == '__main__':

    unittest.main()

