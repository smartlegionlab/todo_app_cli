# --------------------------------------------------------
# Licensed under the terms of the BSD 3-Clause License
# (see LICENSE for details).
# Copyright © 2024, A.A. Suvorov
# All rights reserved.
# --------------------------------------------------------
# https://github.com/smartlegionlab/
# --------------------------------------------------------
from smartlib.db import TaskDatabase
from smartlib.model import Task


class TaskController:

    def __init__(self):
        self.task_database = TaskDatabase('cli_todo_app.db')

    def add_task(self, name):
        task = Task(name=name)
        self.task_database.add_task(task)

    def update_task(self, task):
        return self.task_database.update_task(task)

    def get_all_tasks(self):
        return self.task_database.get_all_tasks()

    def get_active_tasks(self):
        return self.task_database.get_active_tasks()

    def get_completed_tasks(self):
        return self.task_database.get_completed_tasks()

    def mark_task_as_completed(self, task_id):
        self.task_database.mark_task_as_completed(task_id)

    def mark_task_as_incomplete(self, task_id):
        self.task_database.mark_task_as_incomplete(task_id)

    def delete_task(self, task_id):
        self.task_database.delete_task(task_id)

    def get_total_task_count(self):
        return self.task_database.get_total_task_count()

    def get_completed_task_count(self):
        return self.task_database.get_completed_task_count()

    def get_active_task_count(self):
        return self.task_database.get_active_task_count()
