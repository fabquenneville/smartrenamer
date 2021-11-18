#!/usr/bin/env python3

import tkinter.filedialog
import tkinter as tk

from .tools import get_content

class DirectorySelector(tk.LabelFrame):
    def __init__(self, parent, *args, **kwargs):
        tk.LabelFrame.__init__(self, parent, *args, **kwargs)

        self.load_components(parent)

    def load_components(self, window):
        textfield = tk.Entry(self, name="directory_entry")
        textfield.focus()
        button = tk.Button(self, text='Open directory', command=lambda: DirectorySelector.open_directory(window))
        
        textfield.pack(side="left", fill="x", expand=True)
        button.pack(side="right", fill=None, expand=False)

    @staticmethod
    def open_directory(window):
        selected_folder = tkinter.filedialog.askdirectory()
        entry = window.nametowidget("directoryselector.directory_entry")
        entry.delete(0,"end")
        entry.insert(0, selected_folder)

        content = get_content(selected_folder, absolute=False)
        
        before_list = window.nametowidget("comparator_frame.before_frame.before_list")
        after_list = window.nametowidget("comparator_frame.after_frame.after_list")

        before_list.delete(0,'end')
        after_list.delete(0,'end')

        for file in content:
            before_list.insert(tk.END, str(file))
            after_list.insert(tk.END, str(file))