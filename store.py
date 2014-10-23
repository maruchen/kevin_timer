#! /usr/bin/env python
# -*- coding: utf-8 -*-

import os, sys, time
import os.path
import re
import logging
import operator

WATCH_FILENAME = "D:/watch.txt"

class Task(object):

    def __init__(self, task_id=None, thing=None, due_timestamp=None, done=False):
        self.task_id = task_id
        self.thing = thing
        self.due_timestamp = due_timestamp
        self.done = done

    def delay_day(self, nday):
        pass

    def delay_minute(self, nminute):
        pass



class Store(object):

    def __init__(self):
        self.watch_filename = WATCH_FILENAME
        self.tasks = []

    def add_task(self, task):
        """
            return task with task_id
        """
        all_tasks = self.__load_task()
        max_id = self.__find_max_id(all_tasks)
        task.task_id = max_id + 1
        all_tasks.append(task)
        self.__save_task(all_tasks)
        return task

    def update_task(self, task):
        task_id = task.task_id
        all_tasks = self.__load_task()
        new_tasks = [t for t in all_tasks if t.task_id != task_id]
        new_tasks.append(task)
        self.__save_task(new_tasks)

    def get_all_tasks(self):
        return self.__load_task()

    def __find_max_id(self, all_tasks):
        max_id = 0
        for task in all_tasks:
            if task.task_id > max_id:
                max_id = task.task_id
        return max_id

    def __load_task(self):
        all_tasks = []
        if os.path.exists(self.watch_filename) == False:
            return all_tasks

        with open(self.watch_filename) as watch_file:
            lines = watch_file.readlines()
            for line in lines:
                task = self.__deserialize_task_from_line(line)
                all_tasks.append(task)
        return all_tasks

    def __deserialize_task_from_line(self, line):
        tokens = line.split('\t', 3)
        assert(len(tokens) == 4)
        task_id = int(tokens[0])
        done_str = tokens[1]
        done = True if done_str == "D" else False
        due_time= tokens[2]
        due_timestamp = time.mktime(time.strptime(due_time, "%Y-%m-%d %H:%M:%S"))
        thing = tokens[3].strip()
        return Task(task_id, thing, due_timestamp, done)

    def __save_task(self, all_tasks):
        with open(self.watch_filename, 'w') as watch_file:
            lines = []
            for task in all_tasks:
                line = self.__serialize_task_to_line(task) + "\n"
                lines.append(line)
            watch_file.writelines(lines)
        return

    def __serialize_task_to_line(self, task):
        done_str = "D" if task.done else "U"
        return '\t'.join([
                            str(task.task_id),
                            done_str,
                            time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(task.due_timestamp)),
                            task.thing
                        ])


if __name__ == "__main__":
    check_watch_file()




