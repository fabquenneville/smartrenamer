#!/usr/bin/env python3

import tkinter.filedialog
import tkinter as tk

from .directoryselector import DirectorySelector

class MainMenu(tk.Menu):
    def __init__(self, parent, *args, **kwargs):
        tk.Menu.__init__(self, parent, *args, **kwargs)

        self.load_components(parent)

    def load_components(self, mainapp):

        file_menu = tk.Menu(self, tearoff=False)
        file_menu.add_command(
            label='Open directory',
            command=mainapp.load_new_directory
        )
        file_menu.add_command(
            label='Reload directory',
            command=mainapp.load_directory
        )
        file_menu.add_separator()
        file_menu.add_command(
            label='Exit',
            command=self.destroy,
        )
        self.add_cascade(
            label="File",
            menu=file_menu,
            underline=0
        )

        help_menu = tk.Menu(self, tearoff=0)
        help_menu.add_command(label='Welcome')
        help_menu.add_command(label='About...')
        self.add_cascade(
            label="Help",
            menu=help_menu
        )