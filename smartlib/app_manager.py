# --------------------------------------------------------
# Licensed under the terms of the BSD 3-Clause License
# (see LICENSE for details).
# Copyright © 2024, A.A. Suvorov
# All rights reserved.
# --------------------------------------------------------
# https://github.com/smartlegionlab/
# --------------------------------------------------------
from smartlib.controller import TaskController
from smartlib.view import TaskView


class AppManager:
    def __init__(self):
        self.view = TaskView()
        self.controller = TaskController()

    def main_menu(self):
        while True:
            total_task_count = self.controller.get_total_task_count()
            completed_task_count = self.controller.get_completed_task_count()
            active_task_count = self.controller.get_active_task_count()
            self.view.show_menu(
                total_count=total_task_count,
                completed_count=completed_task_count,
                active_count=active_task_count
            )
            self.view.printer.print_center()
            cmd = input('Select the option you want: ')
            if cmd == '1':
                self.add_task()
            elif cmd == '2':
                self.show_task_active()
            elif cmd == '3':
                self.show_task_completed()
            elif cmd == '0':
                break
            else:
                self.view.show_message('Invalid option!')
                self.view.press_enter_to_continue()

    def add_task(self):
        name = self.view.get_task_name()
        self.controller.add_task(name)
        self.view.show_message('Task added!')
        self.view.press_enter_to_continue()

    def show_task_active(self):
        tasks = self.controller.get_active_tasks()
        self.view.printer.print_center(text=f'Active tasks ({len(tasks)}):')
        for task in tasks:
            self.view.show_message(task)
        self.view.printer.print_center()
        self.view.press_enter_to_continue()

    def show_task_completed(self):
        tasks = self.controller.get_completed_tasks()
        self.view.printer.print_center(text=f'Completed tasks ({len(tasks)}):')
        for task in tasks:
            self.view.show_message(task)
        self.view.printer.print_center()
        self.view.press_enter_to_continue()

    def run(self):
        self.view.show_head()
        self.main_menu()
        self.view.show_footer()
