# --------------------------------------------------------
# Licensed under the terms of the BSD 3-Clause License
# (see LICENSE for details).
# Copyright © 2024, A.A. Suvorov
# All rights reserved.
# --------------------------------------------------------
# https://github.com/smartlegionlab/
# --------------------------------------------------------
from smartlib.config import Config
from smartlib.printer import SmartPrinter


class TaskView:
    printer = SmartPrinter()
    config = Config()

    def show_head(self):
        self.printer.show_head(text=self.config.name)

    def show_footer(self):
        self.printer.show_footer(url=self.config.url, copyright_=self.config.copyright_)

    def show_menu(self, total_count, active_count, completed_count):
        self.printer.print_center(text=f'Tasks ({total_count}):')
        print('1. Add new task')
        print(f'2. Active tasks [{active_count}]')
        print(f'3. Completed tasks [{completed_count}]')
        print('0. Exit')

    @staticmethod
    def show_message(message):
        print(message)

    @staticmethod
    def press_enter_to_continue():
        input('Press Enter to continue...')

    def show_error(self, title='ERROR!!!', text='Error! Invalid input.'):
        self.printer.print_center(text=title)
        print(text)
        self.press_enter_to_continue()

    def get_task_name(self):
        while True:
            self.printer.print_center(text='Task name:')
            name = input('Name: ')
            if not name:
                self.show_error(text='Error! Name cannot be empty.')
                continue
            return name
