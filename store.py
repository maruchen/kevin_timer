#! /usr/bin/env python
# -*- coding: utf-8 -*-

import os, sys, time
import os.path
import re
import logging
import operator

POOL_INTERVAL_SECONDS = 60
WATCH_FILENAME = "D:/watch.txt"

class Task(object):

    def __init__(self):
        self.thing = ""
        self.due_timestamp = 0
        self.done = 0



    def __serialize(self):
        return '\t'.join([
                            self.thing,
                            time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(self.due_timestamp))
                            str(self.done)
                        ])

    def __deserialize(self):
        pass

    def __repr__(self):
        return '\t'.join([
                            self.thing,
                            time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(self.due_timestamp))
                            str(self.done)
                        ])


class Store(object):

    def init(self, filename):
        self.watch_filename = filename

    def add_task(self, due_timestamp, thing):
        pass
    with open(WATCH_FILENAME, 'a') as watch_file:
        watch_file.write(input_todo + "\t@ " + time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(absolute_timestamp)) + " (" + str(absolute_timestamp) + ")\n")

    def finish_task(self, due_timestamp, thing):
        pass

    def modify_task(self, due_timestamp, thing, delay_seconds):
        pass

    def get_all_tasks(self):
        pass

    def __load_file(self):
        # TODO: 需要加文件锁
        with open(self.watch_filename) as watch_file:
            lines = watch_file.readlines()
        return lines

    def __save_file(self, lines):
        # TODO: 需要加文件锁
        with open(self.watch_filename, "w") as watch_file:
            watch_file.writelines(lines)
        return

    def __format_task_to_line(self, due_timestamp, thing, done):

if __name__ == "__main__":
    check_watch_file()




