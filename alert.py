#! /usr/bin/env python
# -*- coding: utf-8 -*-

import os, sys, time
import os.path
import fileinput
import re
import logging
import argparse
import operator
import math
from Tkinter import *
from store import *
import threading

POOL_INTERVAL_SECONDS = 60


class AlertDialog(Frame):
    def __init__(self, alert_manager, task, master=None):
        Frame.__init__(self, master)
        self.alert_manager = alert_manager
        self.task = task
        self.due_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(task.due_timestamp))
        self.thing = task.thing
        self._createWidgets()
        self.pack()

    def _createWidgets(self):
        self.timeLabel = Label(self, text=self.due_time)
        self.timeLabel.pack()
        # tkinter 显示utf8.但是从windows cmd读进来的是gbk
        utf8str = self.thing.decode('gbk').encode('utf8')
        self.todoLabel = Label(self, text=utf8str)
        self.todoLabel.pack()
        #self.quitButton = Button(self, text='Quit', command=self.quit)
        #self.quitButton.pack()

        self.delay5DayButton = Button(self, text='5day later', command=self.delay5day)
        self.delay5DayButton.pack()

        self.delay1DayButton = Button(self, text='1day later', command=self.delay1day)
        self.delay1DayButton.pack()

        self.delay1HourButton = Button(self, text='1hour later', command=self.delay1hour)
        self.delay1HourButton.pack()

        self.delay10MinuteButton = Button(self, text='10min later', command=self.delay10min)
        self.delay10MinuteButton.pack()

        self.finishButton = Button(self, text='done!', command=self.done)
        self.finishButton.pack()

    def quit(self):
        self.alert_manager.is_showing = False
        Frame.quit(self)

    def delay5day(self):
        self.task.due_timestamp = self.task.due_timestamp + 24 * 60 * 60 * 5
        store = Store()
        store.update_task(self.task)
        self.quit()

    def delay1day(self):
        self.task.due_timestamp = self.task.due_timestamp + 24 * 60 * 60 * 1
        store = Store()
        store.update_task(self.task)
        self.quit()


    def delay1hour(self):
        self.task.due_timestamp = self.task.due_timestamp + 60 * 60 * 1
        store = Store()
        store.update_task(self.task)
        self.quit()


    def delay10min(self):
        self.task.due_timestamp = self.task.due_timestamp + 60 * 10
        store = Store()
        store.update_task(self.task)
        self.quit()


    def done(self):
        self.task.done = True
        store = Store()
        store.update_task(self.task)
        self.quit()



class AlertManager(object):
    """
    每个进程只能有一个Alert对象
    """
    def __init__(self):
        self.is_showing = False

    def showAlert(self, task):
        if self.is_showing:
            return

        else:
            self.is_showing = True
            self._showDialog(task)

    def _showDialog(self, task):
        root = Tk()
        root.title = "提醒"
        root.lift()
        app = AlertDialog(self, task, master=root)
        #app.master.title('提醒')
        app.mainloop()
        root.destroy()


def check_watch_file():
    #print os.path.abspath() 
    alertManager = AlertManager()
    store = Store()
    while True:
        all_tasks = store.get_all_tasks()
        for task in all_tasks:
            if task.done:
                continue
            if task.due_timestamp <= time.time():
                alertManager.showAlert(task)
                #alertManager.showAlert(task.thing,

        time.sleep(POOL_INTERVAL_SECONDS)



if __name__ == "__main__":
    check_watch_file()




