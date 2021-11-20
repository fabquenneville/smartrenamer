#!/usr/bin/env python3

import tkinter as tk

from .tools import get_content

class DirectorySelector(tk.LabelFrame):
    def __init__(self, parent, *args, **kwargs):
        tk.LabelFrame.__init__(
            self, parent,
            text="Current directory",
            name="directoryselector",
            padx=10, pady=10,
            *args, **kwargs
        )

        self.load_components(parent)

    def load_components(self, mainapp):
        textfield = tk.Entry(self, name="directory_entry")
        textfield.focus()
        reload_button = tk.Button(self, text='Reload', command= mainapp.load_directory)
        open_button = tk.Button(self, text='Open directory', command= mainapp.open_directory)
        
        textfield.pack(side="left", fill="x", expand=True)
        reload_button.pack(side="left", fill=None, expand=False)
        open_button.pack(side="right", fill=None, expand=False)