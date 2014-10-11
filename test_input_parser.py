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
                            "timer.py 0m abc",
                            (time.mktime(time.localtime()) + 60 * 0, "abc")
                        ),
                        (
                            "timer.py 5m 中文",
                            (time.mktime(time.localtime()) + 60 * 5, "中文")
                        ),
                        (
                            "timer.py 5 onlynum中文",
                            (time.mktime(time.localtime()) + 60 * 5, "onlynum中文")
                        ),
                        (
                            "timer.py 5",  # 匿名事件
                            (time.mktime(time.localtime()) + 60 * 5, "")
                        ),
                        (
                            "timer.py abc 99m", # 顺序
                            (time.mktime(time.localtime()) + 60 * 99, "abc")
                        ),
                        (
                            "timer.py 中文 空格 99m",
                            (time.mktime(time.localtime()) + 60 * 99, "中文 空格")
                        ),
                        # N days
                        (
                            "timer.py 0d abc space",
                            (time.mktime(time.localtime()) + 24 * 60 * 60 * 0, "abc space")
                        ),
                        (
                            "timer.py 9d abc",
                            (time.mktime(time.localtime()) + 24 * 60 * 60 * 9, "abc")
                        ),
                        (
                            "timer.py 100d abc",
                            (time.mktime(time.localtime()) + 24 * 60 * 60 * 100, "abc")
                        ),
                        (
                            "timer.py 100day abc",
                            (time.mktime(time.localtime()) + 24 * 60 * 60 * 100, "abc")
                        ),
                        (
                            "timer.py 100days abc",
                            (time.mktime(time.localtime()) + 24 * 60 * 60 * 100, "abc")
                        ),
                        (
                            "timer.py abc 100day",
                            (time.mktime(time.localtime()) + 24 * 60 * 60 * 100, "abc")
                        ),
                     ]
        parser = InputParser()
        for test_case in test_cases:
            (due_timestamp, thing) = parser.parse_cmdline(test_case[0])
            self.assertEqual(test_case[1], (due_timestamp, thing))

if __name__ == '__main__':

    unittest.main()

