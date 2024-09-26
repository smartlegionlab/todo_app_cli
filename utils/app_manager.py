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
from utils.task_manager import TodoManagerJSON
from utils.printers import SmartPrinter


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
        while True:
            task_list = self._todo_manager.data["tasks"]
            task_dict = {str(n): task for n, task in enumerate(task_list, 1)}
            self._printer.print_center(f'Task list ({self._todo_manager.count}):')
            if len(task_list):
                for n, task in enumerate(task_list, 1):
                    print(f'{n}. {task["title"]}')
            else:
                print('Tasks not found...')
            print('0. Back')
            self._printer.print_center()
            cmd = input('Select the number of tasks you want: ')

            if cmd == '0':
                break

            if cmd in task_dict.keys():
                self.show_task(task_dict[cmd]["id"])
            else:
                self._show_error(text='Error! Task not found.')

    @staticmethod
    def confirm_action():
        while True:
            user_input = input("Are you sure?? (y/n): ").strip().lower()
            if user_input == 'y':
                return True
            elif user_input == 'n':
                return False
            else:
                print("Please enter 'y' for yes or 'n' for no.")

    def show_task(self, task_id):
        while True:
            self._printer.print_center(text=f'Task {task_id}:')
            task = self._todo_manager.get_task(task_id)
            if task:
                print(f'Title: {task["title"]}')
                print(f'Description: {task["description"]}')
                print(f'Due date: {task["due_date"]}')
                print(f'Completed: {self._get_text_task_status(task["completed"])}')
                self._printer.print_center(text='Select an option:')
                print('1. Edit')
                print('2. Delete')
                print('3. Mark as done')
                print('0. Back')
                self._printer.print_center()
                cmd = input('Select the option you want: ')
                if cmd == '0':
                    break
                elif cmd == '1':
                    self._printer.print_center(f'Update task {task["title"]}:')
                    title = self._update_task_title(task["title"])
                    description = self._update_task_description(task["description"])
                    due_date = self._update_due_date(due_date=task["due_date"])
                    completed = self._update_completed(completed=task["completed"])
                    self._todo_manager.update_task(
                        task_id=task_id,
                        title=title,
                        description=description,
                        due_date=due_date,
                        completed=completed
                    )
                    continue
                elif cmd == '2':
                    self._printer.print_center(f'Delete task {task["title"]}:')
                    delete_flag = self._get_completed()
                    if delete_flag:
                        status = self._todo_manager.delete_task(task["id"])
                        if status:
                            self._printer.print_framed('Task deleted.')
                            break
                        else:
                            self._show_error(text='Error! Task not found.')
                elif cmd == '3':
                    self._printer.print_center(f'Mark as done:')
                    flag = self._get_completed()
                    if flag:
                        self._todo_manager.mark_task_as_completed(task_id)
                        self._printer.print_framed('Task marked as done.')
                    continue
            else:
                self._show_error(text='Error! Task not found.')
            break
        self._continue()

    @staticmethod
    def _get_completed():
        while True:
            cmd = input('Mark task as completed? (y/n): ')
            if cmd == 'y':
                return True
            elif cmd == 'n':
                return False
            else:
                print('Error! Invalid input.')

    @staticmethod
    def _update_task_title(title):
        while True:
            cmd = input('Title: ')
            if not cmd:
                return title
            return cmd

    @staticmethod
    def _update_task_description(description):
        while True:
            cmd = input('Description: ')
            if not cmd:
                return description
            return cmd

    def _update_due_date(self, due_date):
        while True:
            cmd = input('Due date (format: YYYY-MM-DD HH:MM): ')
            if not cmd:
                return due_date
            try:
                datetime.datetime.strptime(cmd, "%Y-%m-%d %H:%M")
            except ValueError:
                self._show_error(text='Error! Due date must be in the format "YYYY-MM-DD HH:MM".')
                continue
            return cmd

    @staticmethod
    def _update_completed(completed):
        while True:
            cmd = input('Mark task as completed? (y/n): ')
            if not cmd:
                return completed
            if cmd == 'y':
                return True
            elif cmd == 'n':
                return False
            else:
                print('Error! Invalid input.')

    @staticmethod
    def _get_text_task_status(status):
        if status:
            return 'Yes'
        else:
            return 'No'

    def _continue(self):
        self._printer.print_framed('Press enter to continue... ')
        input()

    def run(self):
        self.show_head()
        self.main_menu()
        self.show_footer()
