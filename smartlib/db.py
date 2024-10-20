# --------------------------------------------------------
# Licensed under the terms of the BSD 3-Clause License
# (see LICENSE for details).
# Copyright © 2024, A.A. Suvorov
# All rights reserved.
# --------------------------------------------------------
# https://github.com/smartlegionlab/
# --------------------------------------------------------
import os
import sqlite3
from smartlib.model import Task


class TaskDatabase:
    user_home = os.path.expanduser("~")

    def __init__(self, db_name):
        self.db_name = os.path.join(self.user_home, db_name)
        self.connection = sqlite3.connect(self.db_name)
        self.create_table()

    def create_table(self):
        with self.connection:
            self.connection.execute('''
                CREATE TABLE IF NOT EXISTS tasks (
                    id TEXT PRIMARY KEY,
                    name TEXT NOT NULL,
                    completed BOOLEAN NOT NULL
                )
            ''')

    def add_task(self, task):
        with self.connection:
            self.connection.execute('''
                INSERT INTO tasks (id, name, completed) VALUES (?, ?, ?)
            ''', (task.id, task.name, task.completed))

    def get_completed_tasks(self):
        cursor = self.connection.cursor()
        cursor.execute('SELECT id, name, completed FROM tasks WHERE completed')
        rows = cursor.fetchall()
        return [Task(task_id=row[0], name=row[1], completed=row[2]) for row in rows]

    def get_active_tasks(self):
        cursor = self.connection.cursor()
        cursor.execute('SELECT id, name, completed FROM tasks WHERE NOT completed')
        rows = cursor.fetchall()
        return [Task(task_id=row[0], name=row[1], completed=row[2]) for row in rows]

    def get_all_tasks(self):
        cursor = self.connection.cursor()
        cursor.execute('SELECT id, name, completed FROM tasks')
        rows = cursor.fetchall()
        return [Task(task_id=row[0], name=row[1], completed=row[2]) for row in rows]

    def update_task(self, task):
        with self.connection:
            self.connection.execute('''
                UPDATE tasks SET name = ?, completed = ? WHERE id = ?
            ''', (task.name, task.completed, task.id))

    def mark_task_as_completed(self, task_id):
        with self.connection:
            self.connection.execute('''
                UPDATE tasks SET completed = ? WHERE id = ?
            ''', (True, task_id))

    def mark_task_as_incomplete(self, task_id):
        with self.connection:
            self.connection.execute('''
                UPDATE tasks SET completed = ? WHERE id = ?
            ''', (False, task_id))

    def delete_task(self, task_id):
        with self.connection:
            self.connection.execute('DELETE FROM tasks WHERE id = ?', (task_id,))

    def get_task_counts(self):
        cursor = self.connection.cursor()
        cursor.execute('SELECT COUNT(*) FROM tasks')
        total_count = cursor.fetchone()[0]

        cursor.execute('SELECT COUNT(*) FROM tasks WHERE completed = ?', (True,))
        completed_count = cursor.fetchone()[0]

        cursor.execute('SELECT COUNT(*) FROM tasks WHERE completed = ?', (False,))
        active_count = cursor.fetchone()[0]

        return total_count, completed_count, active_count

    def get_total_task_count(self):
        cursor = self.connection.cursor()
        cursor.execute('SELECT COUNT(*) FROM tasks')
        return cursor.fetchone()[0]

    def get_completed_task_count(self):
        cursor = self.connection.cursor()
        cursor.execute('SELECT COUNT(*) FROM tasks WHERE completed = ?', (True,))
        return cursor.fetchone()[0]

    def get_active_task_count(self):
        cursor = self.connection.cursor()
        cursor.execute('SELECT COUNT(*) FROM tasks WHERE completed = ?', (False,))
        return cursor.fetchone()[0]

    def close(self):
        self.connection.close()
