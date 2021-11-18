#!/usr/bin/env python3

import tkinter as tk

class OperationSelector(tk.LabelFrame):
    def __init__(self, parent, *args, **kwargs):
        tk.LabelFrame.__init__(
            self, parent,
            text="Operations",
            name="operationselector",
            padx=10, pady=10,
            *args, **kwargs
        )

        self.action = tk.StringVar()

        self.load_components(parent)

    def load_components(self, parent):
        radiobutton_widget1 = tk.Radiobutton(
            self,
            text="Clean",
            variable=self.action,
            value="clean",
            command=lambda: (
                parent.reload_subcomponents(),
            )
        )
        radiobutton_widget2 = tk.Radiobutton(
            self,
            text="Replace",
            variable=self.action,
            value="replace",
            command=lambda: (
                parent.reload_subcomponents(),
            )
        )
        radiobutton_widget1.pack(side="left")
        radiobutton_widget2.pack(side="left")
        radiobutton_widget1.select()

    def get_action(self):
        return self.action.get()