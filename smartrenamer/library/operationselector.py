#!/usr/bin/env python3

import tkinter as tk

class OperationSelector(tk.LabelFrame):
    def __init__(self, parent, *args, **kwargs):
        tk.LabelFrame.__init__(
            self, parent,
            text="Operations",
            name="optionselector",
            padx=10, pady=10,
            *args, **kwargs
        )

        self.action = tk.IntVar()

        self.load_components()
        self.reload_subcomponents()

    def load_components(self):
        radiobutton_widget1 = tk.Radiobutton(self,
            text="Clean",
            variable=self.action,
            value="clean"
        )
        radiobutton_widget2 = tk.Radiobutton(self,
            text="Replace",
            variable=self.action,
            value="replace"
        )
        radiobutton_widget1.pack(side="left")
        radiobutton_widget2.pack(side="left")
        radiobutton_widget1.select()

    def reload_subcomponents(self):
        pass

    def get_action(self):
        return self.action.get()