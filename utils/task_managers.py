# --------------------------------------------------------
# Licensed under the terms of the BSD 3-Clause License
# (see LICENSE for details).
# Copyright © 2024, A.A. Suvorov
# All rights reserved.
# --------------------------------------------------------
# https://github.com/smartlegionlab/
# --------------------------------------------------------
import datetime
import json
import os
import sqlite3
import uuid


class Task:
    def __init__(self, title, description, due_date, completed=False):
        self.id = str(uuid.uuid4())
        self.title = title
        self.description = description
        self.due_date = due_date
        self.completed = completed
        self.created_at = datetime.datetime.now().isoformat()
        self.updated_at = datetime.datetime.now().isoformat()

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'due_date': self.due_date,
            'completed': self.completed,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }

    @classmethod
    def from_dict(cls, data):
        task = cls(
            title=data['title'],
            description=data['description'],
            due_date=data['due_date'],
            completed=data['completed']
        )
        task.id = data['id']
        task.created_at = data['created_at']
        task.updated_at = data['updated_at']
        return task


class TaskManagerJSON:
    def __init__(self, filename='todo.json'):
        self.filename = filename
        self.tasks = []
        self.load()

    @property
    def count(self):
        return len(self.tasks)

    def load(self):
        if os.path.exists(self.filename) and os.path.getsize(self.filename) > 0:
            with open(self.filename, 'r') as f:
                data = json.load(f)
                self.tasks = [Task.from_dict(task_data) for task_data in data['tasks']]
        else:
            self.tasks = []

    def save(self):
        with open(self.filename, 'w') as f:
            json.dump({'tasks': [task.to_dict() for task in self.tasks]}, f, indent=4)

    def create_task(self, title, description, due_date, completed=False):
        title = self.get_unique_title(title)
        task = Task(title, description, due_date, completed)
        self.tasks.append(task)
        self.save()
        return True

    def get_unique_title(self, title):
        existing_titles = {task.title for task in self.tasks}
        if title not in existing_titles:
            return title

        count = 1
        new_title = f"{title} ({count})"
        while new_title in existing_titles:
            count += 1
            new_title = f"{title} ({count})"

        return new_title

    def read_tasks(self):
        return self.tasks

    def get_task(self, task_id):
        for task in self.tasks:
            if task.id == task_id:
                return task
        return None

    def update_task(self, task_id, title=None, description=None, due_date=None, completed=None):
        for task in self.tasks:
            if task.id == task_id:
                if title is not None:
                    task.title = self.get_unique_title(title)
                if description is not None:
                    task.description = description
                if due_date is not None:
                    task.due_date = due_date
                if completed is not None:
                    task.completed = completed
                task.updated_at = datetime.datetime.now().isoformat()
                self.save()
                return True
        return False

    def delete_task(self, task_id):
        for task in self.tasks:
            if task.id == task_id:
                self.tasks.remove(task)
                self.save()
                return True
        return False

    def mark_task_as_completed(self, task_id):
        for task in self.tasks:
            if task.id == task_id:
                task.completed = True
                task.updated_at = datetime.datetime.now().isoformat()
                self.save()
                return True
        return False


class TaskManagerSQLite:
    def __init__(self, db_name='todo.db'):
        self.db_name = db_name
        self.connection = sqlite3.connect(self.db_name)
        self.cursor = self.connection.cursor()
        self.create_table()
        self.tasks = self.load()

    def create_table(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS tasks (
                id TEXT PRIMARY KEY,
                title TEXT NOT NULL,
                description TEXT,
                due_date TEXT,
                completed BOOLEAN NOT NULL,
                created_at TEXT NOT NULL,
                updated_at TEXT NOT NULL
            )
        ''')
        self.connection.commit()

    @property
    def count(self):
        return len(self.tasks)

    def load(self):
        self.cursor.execute('SELECT * FROM tasks')
        return [
            Task.from_dict({
                'id': row[0],
                'title': row[1],
                'description': row[2],
                'due_date': row[3],
                'completed': row[4],
                'created_at': row[5],
                'updated_at': row[6]
            })
            for row in self.cursor.fetchall()
        ]

    def save(self):
        self.connection.commit()

    def create_task(self, title, description, due_date, completed=False):
        title = self.get_unique_title(title)
        task = Task(title, description, due_date, completed)
        self.cursor.execute('''
            INSERT INTO tasks (id, title, description, due_date, completed, created_at, updated_at)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (task.id, task.title, task.description, task.due_date, task.completed, task.created_at, task.updated_at))
        self.save()
        self.tasks = self.load()
        return True

    def get_unique_title(self, title):
        self.cursor.execute('SELECT title FROM tasks')
        existing_titles = {row[0] for row in self.cursor.fetchall()}
        if title not in existing_titles:
            return title

        count = 1
        new_title = f"{title} ({count})"
        while new_title in existing_titles:
            count += 1
            new_title = f"{title} ({count})"

        return new_title

    def read_tasks(self):
        return self.tasks

    def get_task(self, task_id):
        self.cursor.execute('SELECT * FROM tasks WHERE id = ?', (task_id,))
        row = self.cursor.fetchone()
        if row:
            return Task.from_dict({
                'id': row[0],
                'title': row[1],
                'description': row[2],
                'due_date': row[3],
                'completed': row[4],
                'created_at': row[5],
                'updated_at': row[6]
            })
        return None

    def update_task(self, task_id, title=None, description=None, due_date=None, completed=None):
        task = self.get_task(task_id)
        if not task:
            return False

        if title is not None:
            title = self.get_unique_title(title)
        else:
            title = task.title

        if description is None:
            description = task.description
        if due_date is None:
            due_date = task.due_date
        if completed is None:
            completed = task.completed

        updated_at = datetime.datetime.now().isoformat()
        self.cursor.execute('''
            UPDATE tasks
            SET title = ?, description = ?, due_date = ?, completed = ?, updated_at = ?
            WHERE id = ?
        ''', (title, description, due_date, completed, updated_at, task_id))
        self.save()
        self.tasks = self.load()
        return True

    def delete_task(self, task_id):
        self.cursor.execute('DELETE FROM tasks WHERE id = ?', (task_id,))
        self.save()
        self.tasks = self.load()
        return True

    def mark_task_as_completed(self, task_id):
        self.cursor.execute('UPDATE tasks SET completed = ? WHERE id = ?', (True, task_id))
        self.save()
        self.tasks = self.load()
        return True

    def close(self):
        self.connection.close()
