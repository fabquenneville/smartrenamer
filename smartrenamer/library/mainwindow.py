#!/usr/bin/env python3

import tkinter.filedialog
import tkinter as tk

from .mainmenu import MainMenu
from .directoryselector import DirectorySelector
from .comparator import Comparator

class MainWindow(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        self.mainmenu = None
        self.directoryselector = None
        self.comparator = None

        self.build_component()
        self.config(menu=self.mainmenu)

    def build_component(self):
        self.title("smartrenamer")
        w, h = self.winfo_screenwidth(), self.winfo_screenheight()
        self.geometry("%dx%d+0+0" % (w, h))

        self.mainmenu = MainMenu(self)
        self.directoryselector = DirectorySelector(
            self,
            text="Current directory",
            name="dir_selector_frame",
            padx=10,
            pady=10
        )
        self.comparator = Comparator(
            self,
            name="comparator_frame",
            pady=10
        )

        self.directoryselector.pack(fill="x")
        self.comparator.pack(expand=True, fill="both")
