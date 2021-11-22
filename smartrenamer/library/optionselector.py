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
            padx=10,
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
            padx=10,
        )
        self.wordmanager = WordManager(self)

        self.operationselector.grid(row=0, column=0, sticky="new")
        self.operationoptionsselector.grid(row=0, column=1, sticky="new")
        self.wordmanager.grid(row=1, column=0, columnspan=2, sticky="sew")

    def reload_subcomponents(self):
        mainapp = self.winfo_toplevel()
        config = mainapp.get_config()
        separators_from = config["main"]["separators_from"]
        separators_to = config["main"]["separators_to"]

        for child in self.operationoptionsselector.winfo_children():
            child.destroy()
        
        action = self.operationselector.get_action()
        if action == "clean":
            self.operationoptions = {
                "autoremove":               tk.IntVar(),
                "unify_separators":         tk.IntVar(),
                "unify_separators_from":    tk.StringVar(),
                "unify_separators_to":      tk.StringVar(),
                "unify_brackets":           tk.IntVar(),
                "unify_brackets_type":           tk.StringVar(),
            }

            autoremove_checkbutton = tk.Checkbutton(
                self.operationoptionsselector,
                text = "Auto remove",
                variable = self.operationoptions["autoremove"],
                onvalue = 1, offvalue = 0
            )
            autoremove_checkbutton.select()

            unify_separators_checkbutton = tk.Checkbutton(
                self.operationoptionsselector,
                text = "Unify Separators",
                variable = self.operationoptions["unify_separators"],
                onvalue = 1, offvalue=0
            )
            unify_separators_checkbutton.select()

            unify_separators_from_label = tk.Label(
                self.operationoptionsselector,
                text = "From:"
            )
            unify_separators_from = tk.Entry(
                self.operationoptionsselector,
                name = "unify_separators_from",
                textvariable = self.operationoptions["unify_separators_from"]
            )
            if separators_from:
                unify_separators_from.insert(tk.END, separators_from)

            unify_separators_to_label = tk.Label(
                self.operationoptionsselector,
                text = "To"
            )
            unify_separators_to = tk.Entry(
                self.operationoptionsselector,
                name = "unify_separators_to",
                textvariable = self.operationoptions["unify_separators_to"]
            )
            if separators_to:
                unify_separators_to.insert(tk.END, separators_to)

            unify_brackets_checkbutton = tk.Checkbutton(
                self.operationoptionsselector,
                text = "Unify Brackets",
                variable = self.operationoptions["unify_brackets"],
                onvalue = 1, offvalue=0
            )
            unify_brackets_checkbutton.select()

            unify_brackets_parentheses = tk.Radiobutton(
                self.operationoptionsselector,
                text="()",
                variable = self.operationoptions["unify_brackets_type"],
                value="parentheses"
            )
            unify_brackets_parentheses.select()
            unify_brackets_squares = tk.Radiobutton(
                self.operationoptionsselector,
                text="[]",
                variable = self.operationoptions["unify_brackets_type"],
                value="squares"
            )
            unify_brackets_curly = tk.Radiobutton(
                self.operationoptionsselector,
                text="{}",
                variable = self.operationoptions["unify_brackets_type"],
                value="curly"
            )
            unify_brackets_angles = tk.Radiobutton(
                self.operationoptionsselector,
                text="<>",
                variable = self.operationoptions["unify_brackets_type"],
                value="angles"
            )






            autoremove_checkbutton.pack(side="left")
            unify_separators_checkbutton.pack(side="left")
            unify_separators_from_label.pack(side="left")
            unify_separators_from.pack(side="left")
            unify_separators_to_label.pack(side="left")
            unify_separators_to.pack(side="left")
            unify_brackets_checkbutton.pack(side="left")
            unify_brackets_parentheses.pack(side="left")
            unify_brackets_squares.pack(side="left")
            unify_brackets_curly.pack(side="left")
            unify_brackets_angles.pack(side="left")
        

    def get_action(self):
        return self.action.get()