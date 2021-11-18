#!/usr/bin/env python3

import tkinter as tk

from .mainmenu import MainMenu
from .directoryselector import DirectorySelector
from .operationselector import OperationSelector
from .comparator import Comparator

class MainApplication(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        self.colors = None
        self.mainmenu = None
        self.directoryselector = None
        self.operationselector = None
        self.comparator = None

        self.load_components()

    def load_components(self):
        self.title("smartrenamer")
        w, h = self.winfo_screenwidth(), self.winfo_screenheight()
        self.geometry("%dx%d+0+0" % (w, h))

        self.mainmenu = MainMenu(self)

        self.directoryselector = DirectorySelector(
            self,
            text="Current directory",
            name="directoryselector",
            padx=10,
            pady=10
        )

        self.operationselector = OperationSelector(
            self,
            text="Operations",
            name="operationselector",
            padx=10,
            pady=10
        )

        self.comparator = Comparator(
            self,
            name="comparator_frame",
            pady=10
        )

        self.directoryselector.pack(fill="x")
        self.operationselector.pack(fill="x")
        self.comparator.pack(expand=True, fill="both")

        self.config(menu=self.mainmenu)

        # Theme.set_colors(self)