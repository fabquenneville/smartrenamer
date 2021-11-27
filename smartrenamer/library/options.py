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
        self.variables = {
            "remove_words":                 tk.IntVar(),
            "unify_capitalisation":         tk.IntVar(),
            "unify_capitalisation_type":    tk.StringVar(),
            "unify_dates":                  tk.IntVar(),
            "unify_dates_format":           tk.StringVar(),
            "unify_dates_separators":       tk.IntVar(),
            "unify_dates_separators_type":  tk.StringVar(),
            "unify_dates_brackets":         tk.IntVar(),
            "unify_dates_brackets_type":    tk.StringVar(),
            "unify_separators":             tk.IntVar(),
            "unify_separators_from":        tk.StringVar(),
            "unify_separators_to":          tk.StringVar(),
            "unify_brackets":               tk.IntVar(),
            "unify_brackets_type":          tk.StringVar(),
        }

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
                tk.Frame(
                    self.operationoptionsselector,
                    name = "unify_dates_frame",
                    # borderwidth = 1, relief = tk.SOLID
                ),
                tk.Frame(
                    self.operationoptionsselector,
                    name = "unify_dates_separators_frame",
                    # borderwidth = 1, relief = tk.SOLID
                ),
                tk.Frame(
                    self.operationoptionsselector,
                    name = "unify_dates_brackets_frame",
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

                if component._name == "misc_options":
                    subcomponents = [
                        tk.Checkbutton(
                            component,
                            text = "Remove words",
                            name = "remove_words",
                            variable = self.variables["remove_words"],
                            onvalue = 1, offvalue = 0
                        ),
                    ]
                    for subcomponent in subcomponents:
                        if subcomponent._name in ["remove_words"]:
                            subcomponent.select()

                        subcomponent.pack(side="left")

                if component._name == "unify_separators_frame":
                    subcomponents = [
                        tk.Checkbutton(
                            component,
                            text = "Unify Separators",
                            name = "unify_separators",
                            variable = self.variables["unify_separators"],
                            onvalue = 1, offvalue=0
                        ),
                        tk.Label(
                            component,
                            text = "From:"
                        ),
                        tk.Entry(
                            component,
                            name = "unify_separators_from",
                            textvariable = self.variables["unify_separators_from"],
                            width = 10
                        ),
                        tk.Label(
                            component,
                            text = "To"
                        ),
                        tk.Entry(
                            component,
                            name = "unify_separators_to",
                            textvariable = self.variables["unify_separators_to"],
                            width = 10
                        ),
                    ]
                    # subcomponents += WordManager.get_separators_radios(
                    #     parent = component,
                    #     variable = self.variables["unify_separators_type"]
                    # )
                    for subcomponent in subcomponents:
                        if subcomponent._name in ["unify_separators", "space"]:
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
                            variable = self.variables["unify_capitalisation"],
                            onvalue = 1, offvalue=0
                        ),
                        tk.Radiobutton(
                            component,
                            text="Capitalize",
                            name = "capitalize",
                            variable = self.variables["unify_capitalisation_type"],
                            value="capitalize"
                        ),
                        tk.Radiobutton(
                            component,
                            text="UPPER",
                            name = "upper",
                            variable = self.variables["unify_capitalisation_type"],
                            value="upper"
                        ),
                        tk.Radiobutton(
                            component,
                            text="lower",
                            name = "lower",
                            variable = self.variables["unify_capitalisation_type"],
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
                            variable = self.variables["unify_brackets"],
                            onvalue = 1, offvalue=0
                        ),
                    ]
                    subcomponents += WordManager.get_brackets_radios(
                        parent = component,
                        variable = self.variables["unify_brackets_type"]
                    )
                    for subcomponent in subcomponents:
                        if subcomponent._name in ["unify_brackets", "parenthese"]:
                            subcomponent.select()
                        subcomponent.pack(side="left")


                if component._name == "unify_dates_frame":
                    subcomponents = [
                        tk.Checkbutton(
                            component,
                            text = "Unify date formats",
                            name = "unify_dates",
                            variable = self.variables["unify_dates"],
                            onvalue = 1, offvalue=0
                        ),
                        tk.Radiobutton(
                            component,
                            text = "YYYY-MM-DD",
                            name = "yymd",
                            variable = self.variables["unify_dates_format"],
                            value="yymd"
                        ),
                        tk.Radiobutton(
                            component,
                            text = "YY-MM-DD",
                            name = "ymd",
                            variable = self.variables["unify_dates_format"],
                            value="ymd",
                        ),
                        tk.Radiobutton(
                            component,
                            text = "DD-MM-YYYY",
                            name ="dmyy",
                            variable = self.variables["unify_dates_format"],
                            value="dmyy"
                        ),
                        tk.Radiobutton(
                            component,
                            text = "DD-MM-YY",
                            name = "dmy",
                            variable = self.variables["unify_dates_format"],
                            value="dmy",
                        ),
                    ]
                    for subcomponent in subcomponents:
                        if subcomponent._name in ["unify_dates", "yymd"]:
                            subcomponent.select()
                        subcomponent.pack(side="left")


                if component._name == "unify_dates_separators_frame":
                    subcomponents = [
                        tk.Checkbutton(
                            component,
                            text = "Unify date separators",
                            name = "unify_dates_separators",
                            variable = self.variables["unify_dates_separators"],
                            onvalue = 1, offvalue=0
                        ),
                    ]
                    subcomponents += WordManager.get_separators_radios(
                        parent = component,
                        variable = self.variables["unify_dates_separators_type"]
                    )
                    for subcomponent in subcomponents:
                        if subcomponent._name in ["unify_dates_separators", "dash"]:
                            subcomponent.select()
                        subcomponent.pack(side="left")


                if component._name == "unify_dates_brackets_frame":
                    subcomponents = [
                        tk.Checkbutton(
                            component,
                            text = "Unify date brackets",
                            name = "unify_dates_brackets",
                            variable = self.variables["unify_dates_brackets"],
                            onvalue = 1, offvalue=0
                        ),
                    ]
                    subcomponents += WordManager.get_brackets_radios(
                        parent = component,
                        variable = self.variables["unify_dates_brackets_type"]
                    )
                    for subcomponent in subcomponents:
                        if subcomponent._name in ["unify_dates_brackets", "parenthese"]:
                            subcomponent.select()
                        subcomponent.pack(side="left")

    def get_variables(self):
        return {
            "remove_words":                 self.variables["remove_words"].get(),
            "unify_capitalisation":         self.variables["unify_capitalisation"].get(),
            "unify_capitalisation_type":    self.variables["unify_capitalisation_type"].get(),
            "unify_dates":                  self.variables["unify_dates"].get(),
            "unify_dates_format":           self.variables["unify_dates_format"].get(),
            "unify_dates_separators":       self.variables["unify_dates_separators"].get(),
            "unify_dates_separators_type":  self.variables["unify_dates_separators_type"].get(),
            "unify_dates_brackets":         self.variables["unify_dates_brackets"].get(),
            "unify_dates_brackets_type":    self.variables["unify_dates_brackets_type"].get(),
            "unify_separators":             self.variables["unify_separators"].get(),
            "unify_separators_from":        self.variables["unify_separators_from"].get(),
            "unify_separators_to":          self.variables["unify_separators_to"].get(),
            "unify_brackets":               self.variables["unify_brackets"].get(),
            "unify_brackets_type":          self.variables["unify_brackets_type"].get(),
        }

    def get_action(self):
        return self.action.get()
             
    def get_bracketname(self):
        return self.variables["unify_brackets_type"].get()