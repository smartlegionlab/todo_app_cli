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

    def run(self):
        self._printer.show_head(text=self._config.name)
        self._printer.show_footer(url=self._config.url, copyright_=self._config.copyright_)
