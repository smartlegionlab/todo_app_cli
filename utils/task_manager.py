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


class TodoManagerJSON:
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
