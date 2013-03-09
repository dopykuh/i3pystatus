#!/usr/bin/env python

import sys
import threading

from .core import util, io
from .core.modules import *
from .core.settings import SettingsBase
from .core.config import ConfigFinder

__all__ = [
    "SettingsBase",
    "Module", "AsyncModule", "IntervalModule",
    "Status", "I3statusHandler",
]

def main():
    ConfigFinder().run_config()

class Status:
    def __init__(self, standalone=False, interval=1, input_stream=sys.stdin):
        self.standalone = standalone
        if standalone:
            self.io = io.StandaloneIO(interval)
            self.ce_thread = threading.Thread(target=self.run_command_endpoint)
            self.ce_thread.daemon = True
            self.ce_thread.start()
        else:
            self.io = io.IOHandler(input_stream)

        self.modules = util.ModuleList(self, Module)

    def register(self, module, *args, **kwargs):
        """Register a new module."""

        if module:
            self.modules.append(module, *args, **kwargs)

    def run_command_endpoint(self):
        for j in io.JSONIO(io=io.IOHandler(sys.stdin, io.DevNull()), skiplines=1).read():
            if j["command"] == "block_clicked":
                module = self.modules.get_by_id(j["instance"])
                if module:
                    module.on_click()

    def run(self):
        for j in io.JSONIO(self.io).read():
            for module in self.modules:
                module.inject(j)
I3statusHandler = Status
