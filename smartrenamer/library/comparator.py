#!/usr/bin/env python3

import tkinter as tk

class Comparator(tk.LabelFrame):
    def __init__(self, parent, *args, **kwargs):
        tk.LabelFrame.__init__(self, parent, *args, **kwargs)
        
        self.load_components()

    def load_components(self):
        before_frame = tk.LabelFrame(self, text="Before", name="before_frame", pady=10)
        after_frame = tk.LabelFrame(self, text="After", name="after_frame", pady=10)
        scrollbar = tk.Scrollbar(self)

        before_frame.pack(side="left", expand=True, fill="both")
        after_frame.pack(side="left", expand=True, fill="both")
        scrollbar.pack(side="right", fill="y")
        
        before_list = tk.Listbox(before_frame, yscrollcommand=scrollbar.set, name="before_list")
        after_list = tk.Listbox(after_frame, yscrollcommand=scrollbar.set, name="after_list")

        before_list.pack(side="left", fill="both", expand=True)
        after_list.pack(side="left", fill="both", expand=True)

        scrollbar.config(command=lambda *args: (before_list.yview(*args), after_list.yview(*args)))