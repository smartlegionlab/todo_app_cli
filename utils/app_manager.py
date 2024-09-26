# --------------------------------------------------------
# Licensed under the terms of the BSD 3-Clause License
# (see LICENSE for details).
# Copyright © 2024, A.A. Suvorov
# All rights reserved.
# --------------------------------------------------------
# https://github.com/smartlegionlab/
# --------------------------------------------------------
from utils.configs import Config
from utils.printers import SmartPrinter


class AppManager:

    def __init__(self):
        self._printer = SmartPrinter()
        self._config = Config()

    def show_head(self):
        self._printer.show_head(text=self._config.name)

    def show_footer(self):
        self._printer.show_footer(url=self._config.url, copyright_=self._config.copyright_)

    def main_menu(self):
        while 1:
            self._printer.print_center(text='Main menu:')

            print('1. + Add new task')
            print('2. Task list')
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
        print('Add new task')
        self._continue()

    def show_task_list(self):
        print('Task list')
        self._continue()

    def _continue(self):
        self._printer.print_center()
        input('Press enter to continue... ')

    def run(self):
        self.show_head()
        self.main_menu()
        self.show_footer()
