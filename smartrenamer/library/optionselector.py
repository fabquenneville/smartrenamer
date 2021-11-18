#!/usr/bin/env python3

import tkinter as tk

from .operationselector import OperationSelector
from .wordmanager import WordManager

class OptionSelector(tk.LabelFrame):
    def __init__(self, parent, *args, **kwargs):
        tk.LabelFrame.__init__(
            self, parent,
            text="Options",
            name="optionselector",
            padx=10, pady=10,
            *args, **kwargs
        )
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        self.operationselector = None
        self.operationoptionsselector = None
        self.operationoptions = None

        self.load_components()
        self.reload_subcomponents()

    def load_components(self):
        self.operationselector = OperationSelector(self)
        self.operationoptionsselector = tk.LabelFrame(
            self,
            text="Operation options",
            name="operationoptionsselector",
            padx=10, pady=10,
        )
        self.wordmanager = WordManager(self)

        self.operationselector.grid(row=0, column=0, sticky="new")
        self.operationoptionsselector.grid(row=0, column=1, sticky="new")
        self.wordmanager.grid(row=1, column=0, columnspan=2, sticky="sew")

    def reload_subcomponents(self):
        for child in self.operationoptionsselector.winfo_children():
            child.destroy()
        
        action = self.operationselector.get_action()
        if action == "clean":
            self.operationoptions = {
                "autoremove": tk.IntVar(),
                "unify_markers": tk.IntVar(),
            }

            autoremove_checkbutton = tk.Checkbutton(
                self.operationoptionsselector,
                text="Auto remove",
                variable=self.operationoptions["autoremove"],
                onvalue=1, offvalue=0
            )
            autoremove_checkbutton.select()

            unify_markers_checkbutton = tk.Checkbutton(
                self.operationoptionsselector,
                text="Unify Markers",
                variable=self.operationoptions["unify_markers"],
                onvalue=1, offvalue=0
            )
            unify_markers_checkbutton.select()


            autoremove_checkbutton.pack(side="left")
            unify_markers_checkbutton.pack(side="left")
        

    def get_action(self):
        return self.action.get()