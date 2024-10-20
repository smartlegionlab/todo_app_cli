# --------------------------------------------------------
# Licensed under the terms of the BSD 3-Clause License
# (see LICENSE for details).
# Copyright © 2024, A.A. Suvorov
# All rights reserved.
# --------------------------------------------------------
# https://github.com/smartlegionlab/
# --------------------------------------------------------
import uuid


class Task:
    def __init__(self, name, task_id=None, completed=False):
        self._id = task_id if task_id is not None else str(uuid.uuid4())
        self._name = name
        self._completed = completed

    def mark_as_completed(self):
        self.completed = True

    def mark_as_incomplete(self):
        self.completed = False

    def __repr__(self):
        return self._name

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        self._name = value

    @property
    def completed(self):
        return self._completed

    @completed.setter
    def completed(self, value):
        self._completed = value

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, value):
        self._id = value
