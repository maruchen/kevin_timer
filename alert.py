#! /usr/bin/env python
# -*- coding: utf-8 -*-

import os, sys, time
import fileinput
import re
import logging
import argparse
import operator
import math
from Tkinter import *
import threading

POOL_INTERVAL_SECONDS = 60
WATCH_FILENAME = "watch.txt"


class AlertDialog(Frame):
    def __init__(self, alert_manager, thing, due_time, master=None):
        Frame.__init__(self, master)
        self.alert_manager = alert_manager
        self.thing = thing
        self.due_time = due_time
        self._createWidgets()
        self.pack()

    def _createWidgets(self):
        self.timeLabel = Label(self, text=self.due_time)
        self.timeLabel.pack()
        self.todoLabel = Label(self, text=self.thing)
        self.todoLabel.pack()
        #self.quitButton = Button(self, text='Quit', command=self.quit)
        #self.quitButton.pack()

        self.delay5DayButton = Button(self, text='5day later', command=self.delay5day)
        self.delay5DayButton.pack()

        self.delay1DayButton = Button(self, text='1day later', command=self.delay1day)
        self.delay1DayButton.pack()

        self.delay1HourButton = Button(self, text='1day later', command=self.delay1hour)
        self.delay1HourButton.pack()

        self.delay10MinuteButton = Button(self, text='10min later', command=self.delay10min)
        self.delay10MinuteButton.pack()

        self.finishButton = Button(self, text='done!', command=self.done)
        self.finishButton.pack()

    def quit(self):
        self.alert_manager.is_showing = False
        Frame.quit(self)

    def delay5day(self):
        new_timestamp = time.mktime(time.strptime(self.due_time, "%Y-%m-%d %H:%M:%S")) + 24 * 60 * 60 * 5

        with open(WATCH_FILENAME) as watch_file:
            lines = watch_file.readlines()

        new_lines = []
        for line in lines:
            match = re.match(r'%s\t@ %s\s+' % (self.thing, self.due_time), line)
            if match:
                line = '%s\t@ %s (%.1f)\n' % (self.thing, time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(new_timestamp)), new_timestamp)
            new_lines.append(line)

        with open(WATCH_FILENAME, "w") as watch_file:
            watch_file.writelines(new_lines)

        self.quit()

    def delay1day(self):
        new_timestamp = time.mktime(time.strptime(self.due_time, "%Y-%m-%d %H:%M:%S")) + 24 * 60 * 60 * 1

        with open(WATCH_FILENAME) as watch_file:
            lines = watch_file.readlines()

        new_lines = []
        for line in lines:
            match = re.match(r'%s\t@ %s\s+' % (self.thing, self.due_time), line)
            if match:
                line = '%s\t@ %s (%.1f)\n' % (self.thing, time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(new_timestamp)), new_timestamp)
            new_lines.append(line)

        with open(WATCH_FILENAME, "w") as watch_file:
            watch_file.writelines(new_lines)

        self.quit()

    def delay1hour(self):
        new_timestamp = time.mktime(time.strptime(self.due_time, "%Y-%m-%d %H:%M:%S")) + 60 * 60 * 1

        with open(WATCH_FILENAME) as watch_file:
            lines = watch_file.readlines()

        new_lines = []
        for line in lines:
            match = re.match(r'%s\t@ %s\s+' % (self.thing, self.due_time), line)
            if match:
                line = '%s\t@ %s (%.1f)\n' % (self.thing, time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(new_timestamp)), new_timestamp)
            new_lines.append(line)

        with open(WATCH_FILENAME, "w") as watch_file:
            watch_file.writelines(new_lines)

        self.quit()


    def delay10min(self):
        new_timestamp = time.mktime(time.strptime(self.due_time, "%Y-%m-%d %H:%M:%S")) + 60 * 10

        with open(WATCH_FILENAME) as watch_file:
            lines = watch_file.readlines()

        new_lines = []
        for line in lines:
            match = re.match(r'%s\t@ %s\s+' % (self.thing, self.due_time), line)
            if match:
                line = '%s\t@ %s (%.1f)\n' % (self.thing, time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(new_timestamp)), new_timestamp)
            new_lines.append(line)

        with open(WATCH_FILENAME, "w") as watch_file:
            watch_file.writelines(new_lines)

        self.quit()

    def done(self):
        with open(WATCH_FILENAME) as watch_file:
            lines = watch_file.readlines()

        new_lines = []
        for line in lines:
            match = re.match(r'%s\t@ %s\s+' % (self.thing, self.due_time), line)
            if match:
                line = line[:len(line)-1] + "@\n"
            new_lines.append(line)


        with open(WATCH_FILENAME, "w") as watch_file:
            watch_file.writelines(new_lines)

        self.quit()




class AlertManager(object):
    """
    每个进程只能有一个Alert对象
    """
    def __init__(self):
        self.is_showing = False

    def showAlert(self, thing, due_time):
        if self.is_showing:
            return

        else:
            self.is_showing = True
            self._showDialog(thing, due_time)

    def _showDialog(self, thing, due_time):
        root = Tk()
        app = AlertDialog(self, thing, due_time, master=root)
        #app.master.title('提醒')
        app.mainloop()
        root.destroy()


def check_watch_file():
    alertManager = AlertManager()
    while True:
        with open(WATCH_FILENAME) as watch_file:
            lines = watch_file.readlines()
        for line in lines:
            if line[-2:-1] == "@": # finished task
                continue
            match = re.match(r'(.*)\t@ (.+)\s+\((\d+\.\d+)\)', line)
            if match:
                thing = match.group(1)
                due_time = match.group(2)
                timestamp = float(match.group(3))
                if timestamp <= time.time():
                    alertManager.showAlert(thing, due_time)

        time.sleep(POOL_INTERVAL_SECONDS)



if __name__ == "__main__":
    check_watch_file()




