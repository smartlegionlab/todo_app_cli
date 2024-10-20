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
                self.show_tasks(task_type='active')
            elif cmd == '3':
                self.show_tasks(task_type='completed')
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

    def show_tasks(self, task_type):
        while True:
            if task_type == 'active':
                tasks = self.controller.get_active_tasks()
            else:
                tasks = self.controller.get_completed_tasks()
            if not len(tasks):
                self.view.show_message('No tasks found!')
                self.view.press_enter_to_continue()
                break
            else:
                self.view.show_tasks(tasks=tasks)
                self.view.printer.print_center()
                cmd = input('Select the number of tasks you want: ')

                if cmd == '0':
                    break

                if cmd.isdigit() and 1 <= int(cmd) <= len(tasks):
                    self.show_task(tasks[int(cmd) - 1])
                else:
                    self.view.show_error(text='Error! Task not found.')

    def show_task(self, task):
        while True:
            self.view.show_task(task)
            cmd = input('Select the option you want: ')
            if cmd == '0':
                break
            elif cmd == '1':
                self.view.printer.print_center(f'Update task {task.name}:')
                new_name = self.view.get_task_name()
                task.name = new_name
                self.controller.update_task(task)
                self.view.show_message(f'Task updated.')
                self.view.press_enter_to_continue()
            elif cmd == '2':
                confirm_flag = self.view.confirm_action()
                if confirm_flag:
                    task.completed = not task.completed
                    self.controller.update_task(task)
                    self.view.show_message(f'Successfully updated task {task.name}.')
                    self.view.press_enter_to_continue()
                else:
                    self.view.show_message(f'Action canceled!')
            elif cmd == '3':
                confirm_flag = self.view.confirm_action()
                if confirm_flag:
                    self.controller.delete_task(task.id)
                    self.view.show_message(f'Successfully delete task {task.name}.')
                    self.view.press_enter_to_continue()
                    break
                else:
                    self.view.show_message(f'Action canceled!')

    def run(self):
        self.view.show_head()
        self.main_menu()
        self.view.show_footer()
