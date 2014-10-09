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


class Application(Frame):
    def __init__(self, todo_str, time_str, master=None):
        Frame.__init__(self, master)
        self.pack()
        self.createWidgets(todo_str, time_str)

    def createWidgets(self, todo_str, time_str):
        self.timeLabel = Label(self, text=time_str)
        self.timeLabel.pack()
        self.todoLabel = Label(self, text=todo_str)
        self.todoLabel.pack()
        self.quitButton = Button(self, text='Quit', command=self.quit)
        self.quitButton.pack()



def showDialog(todo_str, time_str):
    app = Application(todo_str, time_str)
    # 设置窗口标题:
    app.master.title('提醒')
    # 主消息循环:
    app.mainloop()



def check_watch_file():
    while True:
        with open("watch.txt") as watch_file:
            for line in watch_file:
                match = re.match(r'(.*)\t@ (.+)\s+\((\d+\.\d+)\)', line)
                if match:
                    todo_str = match.group(1)
                    time_str = match.group(2)
                    timestamp = float(match.group(3))
                    if timestamp >= time.time():
                        showDialog(todo_str, time_str)
        time.sleep(POOL_INTERVAL_SECONDS)




if __name__ == "__main__":
    check_thread = threading.Thread(target=check_watch_file)
    check_thread.deamon = True # this thread will be killed when main thread exits
    check_thread.start()
    
    check_thread.join() # close reading URLs thread




