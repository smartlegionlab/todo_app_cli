# --------------------------------------------------------
# Licensed under the terms of the BSD 3-Clause License
# (see LICENSE for details).
# Copyright © 2024, A.A. Suvorov
# All rights reserved.
# --------------------------------------------------------
# https://github.com/smartlegionlab/
# --------------------------------------------------------


class Config:
    name = 'Cli TODO app'
    url = 'https://github.com/smartlegionlab/'
    copyright_ = 'Copyright © 2024, A.A. Suvorov'
    help_url = 'https://github.com/smartlegionlab/todo_app_cli/'
    db = 'sqlite'  # json | sqlite


class TaskQueries:
    CREATE_TABLE = '''
        CREATE TABLE IF NOT EXISTS tasks (
            id TEXT PRIMARY KEY,
            title TEXT NOT NULL,
            description TEXT,
            due_date TEXT,
            completed BOOLEAN NOT NULL,
            created_at TEXT NOT NULL,
            updated_at TEXT NOT NULL
        )
    '''

    SELECT_ALL_TASKS = 'SELECT * FROM tasks'
    INSERT_TASK = '''
        INSERT INTO tasks (id, title, description, due_date, completed, created_at, updated_at)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    '''
    SELECT_TASK_BY_ID = 'SELECT * FROM tasks WHERE id = ?'
    UPDATE_TASK = '''
        UPDATE tasks
        SET title = ?, description = ?, due_date = ?, completed = ?, updated_at = ?
        WHERE id = ?
    '''
    DELETE_TASK = 'DELETE FROM tasks WHERE id = ?'
    SELECT_TASK_TITLES = 'SELECT title FROM tasks'
    UPDATE_TASK_COMPLETED = 'UPDATE tasks SET completed = ? WHERE id = ?'

