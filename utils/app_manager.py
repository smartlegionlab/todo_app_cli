# --------------------------------------------------------
# Licensed under the terms of the BSD 3-Clause License
# (see LICENSE for details).
# Copyright © 2024, A.A. Suvorov
# All rights reserved.
# --------------------------------------------------------
# https://github.com/smartlegionlab/
# --------------------------------------------------------
import datetime

from utils.configs import Config
from utils.printers import SmartPrinter
from utils.todo_managers import TodoManagerJSON


class AppManager:

    def __init__(self):
        self._printer = SmartPrinter()
        self._config = Config()
        self._todo_manager = TodoManagerJSON()

    def show_head(self):
        self._printer.show_head(text=self._config.name)

    def show_footer(self):
        self._printer.show_footer(url=self._config.url, copyright_=self._config.copyright_)

    def main_menu(self):
        while 1:
            self._printer.print_center(text='Main menu:')

            print('1. Add new task')
            print(f'2. Task list ({self._todo_manager.count})')
            print('0. Exit')

            self._printer.print_center()

            cmd = input('Select the option you want: ')

            if cmd == '1':
                self.add_task()
            elif cmd == '2':
                self.show_task_list()
            elif cmd == '0':
                break
            else:
                self._show_error()

    def _show_error(self, title='ERROR!!!', text='Error! Invalid input.'):
        self._printer.print_center(text=title)
        print(text)
        self._continue()

    def add_task(self):
        self._create_new_task()
        self._continue()

    def _create_new_task(self):
        while True:
            self._printer.print_center(text='New task:')
            title = self._get_title()
            description = self._get_description()
            due_date = self._get_due_date()

            try:
                datetime.datetime.strptime(due_date, "%Y-%m-%d %H:%M")
            except ValueError:
                self._show_error(text='Error! Due date must be in the format "YYYY-MM-DD HH:MM".')
                continue

            status = self._todo_manager.create_task(
                title=title,
                description=description,
                due_date=due_date
            )
            if status:
                print('Task created successfully.')
                break

    def _get_title(self):
        while True:
            title = input('Title: ')
            if not title:
                self._show_error(text='Error! Title cannot be empty.')
                continue
            return title

    def _get_description(self):
        while True:
            description = input('Description: ')
            if not description:
                self._show_error(text='Error! Description cannot be empty.')
                continue
            return description

    def _get_due_date(self):
        while True:
            due_date = input('Due date (format: YYYY-MM-DD HH:MM): ')
            if not due_date:
                self._show_error(text='Error! Due date cannot be empty.')
                continue
            try:
                datetime.datetime.strptime(due_date, "%Y-%m-%d %H:%M")
            except ValueError:
                self._show_error(text='Error! Due date must be in the format "YYYY-MM-DD HH:MM".')
                continue
            return due_date

    def show_task_list(self):
        print('Task list')
        self._continue()

    def _continue(self):
        self._printer.print_framed('Press enter to continue... ')
        input()

    def run(self):
        self.show_head()
        self.main_menu()
        self.show_footer()
