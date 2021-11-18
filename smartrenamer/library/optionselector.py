#!/usr/bin/env python3

import tkinter as tk

from .operationselector import OperationSelector

class OptionSelector(tk.LabelFrame):
    def __init__(self, parent, *args, **kwargs):
        tk.LabelFrame.__init__(
            self, parent,
            text="Options",
            name="optionselector",
            padx=10, pady=10,
            *args, **kwargs
        )

        self.operationselector = None

        self.load_components()
        self.reload_subcomponents()

    def load_components(self):
        self.operationselector = OperationSelector(self)
        self.operationselector.pack(fill="x")

    def reload_subcomponents(self):
        pass

    def get_action(self):
        return self.action.get()