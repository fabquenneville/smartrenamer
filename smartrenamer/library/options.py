#!/usr/bin/env python3

from pprint import pprint
import tkinter as tk

from .wordmanager import WordManager

class Options(tk.LabelFrame):
    def __init__(self, parent, *args, **kwargs):
        tk.LabelFrame.__init__(
            self, parent,
            text = "Options",
            name = "options",
            padx = 10,
            *args, **kwargs
        )

        self.action = tk.StringVar()
        self.operationselector = None
        self.operationoptionsselector = None
        self.operationoptions = None

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        self.load_components()
        self.reload_subcomponents()

    def load_components(self):
        self.operationselector = tk.LabelFrame(
            self,
            text="Operations",
            name="operationselector",
            # padx=10, pady = 1
        )

        operation_buttons = [
            tk.Radiobutton(
                self.operationselector,
                text="Clean",
                variable=self.action,
                value="clean",
                command=lambda: (
                    self.reload_subcomponents(),
                )
            ),
            tk.Radiobutton(
                self.operationselector,
                text="Replace",
                variable=self.action,
                value="replace",
                command=lambda: (
                    self.reload_subcomponents(),
                )
            )
        ]

        operation_buttons[0].select()
        for button in operation_buttons:
            button.pack(side="left")

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
        
        if self.action.get() == "clean":
            self.operationoptions = {
                "autoremove":                   tk.IntVar(),
                "unify_capitalisation":         tk.IntVar(),
                "unify_capitalisation_type":    tk.StringVar(),
                "unify_separators":             tk.IntVar(),
                "unify_separators_from":        tk.StringVar(),
                "unify_separators_to":          tk.StringVar(),
                "unify_brackets":               tk.IntVar(),
                "unify_brackets_type":          tk.StringVar(),
            }

            components = [
                tk.Frame(
                    self.operationoptionsselector,
                    name = "misc_options",
                    # borderwidth = 1, relief = tk.SOLID
                ),
                tk.Frame(
                    self.operationoptionsselector,
                    name = "unify_capitalisation_frame",
                    # borderwidth = 1, relief = tk.SOLID
                ),
                tk.Frame(
                    self.operationoptionsselector,
                    name = "unify_separators_frame",
                    # borderwidth = 1, relief = tk.SOLID
                ),
                tk.Frame(
                    self.operationoptionsselector,
                    name = "unify_brackets_frame",
                    # borderwidth = 1, relief = tk.SOLID
                ),
            ]

            nbcol = 2
            xpos = 0
            ypos = 0

            for i in range(nbcol):
                self.operationoptionsselector.grid_columnconfigure(i, weight=1)
                if i < (len(components) / nbcol):
                    self.operationoptionsselector.grid_rowconfigure(i, weight=1)

            for component in components:

                component.grid(column=xpos, row=ypos, sticky="new", padx = 1, pady = 1)
                xpos += 1
                if xpos > nbcol - 1:
                    xpos = 0
                    ypos += 1

                if component._name in ["autoremove"]:
                    component.select()

                if component._name == "misc_options":
                    subcomponents = [
                        tk.Checkbutton(
                            component,
                            text = "Auto remove",
                            name = "autoremove",
                            variable = self.operationoptions["autoremove"],
                            onvalue = 1, offvalue = 0
                        ),
                    ]
                    for subcomponent in subcomponents:
                        if subcomponent._name in ["autoremove"]:
                            subcomponent.select()
                        subcomponent.pack(side="left")

                if component._name == "unify_separators_frame":
                    subcomponents = [
                        tk.Checkbutton(
                            component,
                            text = "Unify Separators",
                            name = "unify_separators",
                            variable = self.operationoptions["unify_separators"],
                            onvalue = 1, offvalue=0
                        ),
                        tk.Label(
                            component,
                            text = "From:"
                        ),
                        tk.Entry(
                            component,
                            name = "unify_separators_from",
                            textvariable = self.operationoptions["unify_separators_from"],
                            width = 10
                        ),
                        tk.Label(
                            component,
                            text = "To"
                        ),
                        tk.Entry(
                            component,
                            name = "unify_separators_to",
                            textvariable = self.operationoptions["unify_separators_to"],
                            width = 10
                        ),
                    ]
                    for subcomponent in subcomponents:
                        if subcomponent._name in ["unify_separators"]:
                            subcomponent.select()
                        
                        if subcomponent._name == "unify_separators_from" and separators_from:
                            subcomponent.insert(tk.END, separators_from)

                        if subcomponent._name == "unify_separators_to" and separators_to:
                            subcomponent.insert(tk.END, separators_to)
                        subcomponent.pack(side="left")

                if component._name == "unify_capitalisation_frame":
                    subcomponents = [
                        tk.Checkbutton(
                            component,
                            text = "Unify capitalisation",
                            name = "unify_capitalisation",
                            variable = self.operationoptions["unify_capitalisation"],
                            onvalue = 1, offvalue=0
                        ),
                        tk.Radiobutton(
                            component,
                            text="Capitalize",
                            name = "capitalize",
                            variable = self.operationoptions["unify_capitalisation_type"],
                            value="capitalize"
                        ),
                        tk.Radiobutton(
                            component,
                            text="UPPER",
                            name = "upper",
                            variable = self.operationoptions["unify_capitalisation_type"],
                            value="upper"
                        ),
                        tk.Radiobutton(
                            component,
                            text="lower",
                            name = "lower",
                            variable = self.operationoptions["unify_capitalisation_type"],
                            value="lower"
                        ),
                    ]
                    for subcomponent in subcomponents:
                        if subcomponent._name in ["unify_capitalisation", "capitalize"]:
                            subcomponent.select()
                        subcomponent.pack(side="left")
                    

                if component._name == "unify_brackets_frame":
                    subcomponents = [
                        tk.Checkbutton(
                            component,
                            text = "Unify Brackets",
                            name = "unify_brackets",
                            variable = self.operationoptions["unify_brackets"],
                            onvalue = 1, offvalue=0
                        ),
                        tk.Radiobutton(
                            component,
                            text="()",
                            name = "parentheses",
                            variable = self.operationoptions["unify_brackets_type"],
                            value="parentheses"
                        ),
                        tk.Radiobutton(
                            component,
                            text="[]",
                            variable = self.operationoptions["unify_brackets_type"],
                            value="squares"
                        ),
                        tk.Radiobutton(
                            component,
                            text="{}",
                            variable = self.operationoptions["unify_brackets_type"],
                            value="curly"
                        ),
                        tk.Radiobutton(
                            component,
                            text="<>",
                            variable = self.operationoptions["unify_brackets_type"],
                            value="angles"
                        ),
                        tk.Radiobutton(
                            component,
                            text="None",
                            variable = self.operationoptions["unify_brackets_type"],
                            value="none"
                        )
                    ]
                    for subcomponent in subcomponents:
                        if subcomponent._name in ["unify_brackets", "parentheses"]:
                            subcomponent.select()
                        subcomponent.pack(side="left")
                    
                    # component.pack(side="left")


        

    def get_bracketname(self):
        return self.operationoptions["unify_brackets_type"].get()

    def get_operationoptions(self):
        return {
            "autoremove":                   self.operationoptions["autoremove"].get(),
            "unify_capitalisation":         self.operationoptions["unify_capitalisation"].get(),
            "unify_capitalisation_type":    self.operationoptions["unify_capitalisation_type"].get(),
            "unify_separators":             self.operationoptions["unify_separators"].get(),
            "unify_separators_from":        self.operationoptions["unify_separators_from"].get(),
            "unify_separators_to":          self.operationoptions["unify_separators_to"].get(),
            "unify_brackets":               self.operationoptions["unify_brackets"].get(),
            "unify_brackets_type":          self.operationoptions["unify_brackets_type"].get(),
        }

    def get_action(self):
        return self.action.get()