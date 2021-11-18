#!/usr/bin/env python3

import tkinter.filedialog
import tkinter as tk

from .tools import open_directory

class Comparator(tk.LabelFrame):
    def __init__(self, parent, *args, **kwargs):
        tk.LabelFrame.__init__(self, parent, *args, **kwargs)
        # self.component = self.build_component()
        self.build_component(parent)

    def build_component(self, window):
        # mainframe.columnconfigure(0, weight=1)
        # mainframe.columnconfigure(1, weight=1)
        # mainframe.rowconfigure(0, weight=1)

        before_frame = tk.LabelFrame(self, text="Before", name="before_frame", pady=10)
        after_frame = tk.LabelFrame(self, text="After", name="after_frame", pady=10)
        scrollbar = tk.Scrollbar(self)

        # beforeframe.grid(column=0, row=0, sticky="w")
        # afterframe.grid(column=1, row=0, sticky="e")

        # beforeframe.grid(column=0, row=0)
        # afterframe.grid(column=1, row=0)

        before_frame.pack(side="left", expand=True, fill="both")
        after_frame.pack(side="left", expand=True, fill="both")
        scrollbar.pack(side="right", fill="y")

        # beforeframe.pack(side="left", expand=True)
        # afterframe.pack(side="right", expand=True)
        
        before_list = tk.Listbox(before_frame, yscrollcommand=scrollbar.set)
        after_list = tk.Listbox(after_frame, yscrollcommand=scrollbar.set)
        # for line in range(100):
        #     before_list.insert(tk.END, "This is line number " + str(line))
        #     after_list.insert(tk.END, "This is line number " + str(line))

        before_list.pack(side="left", fill="both", expand=True)
        after_list.pack(side="left", fill="both", expand=True)

        scrollbar.config(command=lambda *args: (before_list.yview(*args), after_list.yview(*args)))

        # return main_frame