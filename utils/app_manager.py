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
        print('Welcome to the Cli TODO App!')

    def run(self):
        self.show_head()
        self.main_menu()
        self.show_footer()
