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


class TodoManagerJSON:
    def __init__(self, filename='todo.json'):
        self.filename = filename
        self.data = {'tasks': []}
        self.load()

    @property
    def count(self):
        return len(self.data['tasks'])

    def load(self):
        if os.path.exists(self.filename) and os.path.getsize(self.filename) > 0:
            with open(self.filename, 'r') as f:
                self.data = json.load(f)
        else:
            self.data = {'tasks': []}

    def save(self):
        with open(self.filename, 'w') as f:
            json.dump(self.data, f, indent=4)

    def create_task(self, title, description, due_date, completed=False):
        title = self.get_unique_title(title)
        task_id = str(uuid.uuid4())
        task = {
            'id': task_id,
            'title': title,
            'description': description,
            'due_date': due_date,
            'completed': completed,
            'created_at': datetime.datetime.now().isoformat(),
            'updated_at': datetime.datetime.now().isoformat()
        }
        self.data['tasks'].append(task)
        self.save()
        return True

    def get_unique_title(self, title):
        existing_titles = {task['title'] for task in self.data['tasks']}
        if title not in existing_titles:
            return title

        count = 1
        new_title = f"{title} ({count})"
        while new_title in existing_titles:
            count += 1
            new_title = f"{title} ({count})"

        return new_title

    def read_tasks(self):
        return self.data['tasks']

    def get_task(self, task_id):
        for task in self.data['tasks']:
            if task['id'] == task_id:
                return task
        return None

    def update_task(self, task_id, title=None, description=None, due_date=None, completed=None):
        for task in self.data['tasks']:
            if task['id'] == task_id:
                if title is not None:
                    task['title'] = self.get_unique_title(title)
                if description is not None:
                    task['description'] = description
                if due_date is not None:
                    task['due_date'] = due_date
                if completed is not None:
                    task['completed'] = completed
                task['updated_at'] = datetime.datetime.now().isoformat()
                self.save()
                return True
        return False

    def delete_task(self, task_id):
        for task in self.data['tasks']:
            if task['id'] == task_id:
                self.data['tasks'].remove(task)
                self.save()
                return True
        return False

    def mark_task_as_completed(self, task_id):
        for task in self.data['tasks']:
            if task['id'] == task_id:
                task['completed'] = True
                task['updated_at'] = datetime.datetime.now().isoformat()
                self.save()
                return True
        return False
