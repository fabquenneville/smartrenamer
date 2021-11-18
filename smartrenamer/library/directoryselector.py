#!/usr/bin/env python3

import tkinter.filedialog
import tkinter as tk

from .tools import open_directory

class DirectorySelector(tk.LabelFrame):
    def __init__(self, parent, *args, **kwargs):
        tk.LabelFrame.__init__(self, parent, *args, **kwargs)
        # self.component = self.build_component()
        self.build_component(parent)

    def build_component(self, window):
        # frame = tk.LabelFrame(window, text="Current directory", name="dir_selector_frame", padx=10, pady=10)
        
        textfield = tk.Entry(self, name="directory_entry")
        textfield.focus()
        button = tk.Button(self, text='Open directory', command=lambda: open_directory(window))
        
        textfield.pack(side="left", fill="x", expand=True)
        button.pack(side="right", fill=None, expand=False)

        # return self