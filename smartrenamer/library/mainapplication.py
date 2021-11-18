#!/usr/bin/env python3

import json
import os
from pathlib import Path
import tkinter.filedialog
import tkinter as tk

from .comparator import Comparator
from .directoryselector import DirectorySelector
from .mainmenu import MainMenu
from .optionselector import OptionSelector
from .tools import get_content

class MainApplication(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        self.colors = None
        self.mainmenu = None
        self.directoryselector = None
        self.optionselector = None
        self.comparator = None
        self.userconfig = {
            "main": {
                "selected_folder": None
            }
        }
        self.database = None
        self.directory = None

        self.load_components()
        self.load_config()
        self.load_database()
        self.load_directory()

    def load_components(self):
        self.title("smartrenamer")
        w, h = self.winfo_screenwidth(), self.winfo_screenheight()
        self.geometry("%dx%d+0+0" % (w, h))

        self.mainmenu = MainMenu(self)
        self.directoryselector = DirectorySelector(self)
        self.optionselector = OptionSelector(self)
        self.comparator = Comparator(self)

        self.directoryselector.pack(fill="x")
        self.optionselector.pack(fill="x")
        self.comparator.pack(expand=True, fill="both")

        self.config(menu=self.mainmenu)

        # Theme.set_colors(self)

    @staticmethod
    def get_config_path(createfolders = False):
        homepath = str(Path.home())
        if not homepath[-1] == "/":
            homepath += "/"
        config_folder_path = homepath + ".config/"
        app_config_folder_path = config_folder_path + "smartrenamer/"
        app_config_path = app_config_folder_path + "config.json"

        if not os.path.isdir(config_folder_path) and createfolders:
            os.mkdir(config_folder_path)
        
        if not os.path.isdir(app_config_folder_path) and createfolders:
            os.mkdir(app_config_folder_path)
        
        return app_config_path

    def load_config(self):
        config_path = self.get_config_path()
        if os.path.exists(config_path):
                with open(config_path, 'r') as configfile:
                    self.userconfig = json.load(configfile)

    def save_config(self):
        config_path = self.get_config_path(True)
        with open(config_path, 'w') as configfile:
            json.dump(self.userconfig, configfile, indent=4)

    def load_database(self):
        pass

    def load_directory(self):
        if self.userconfig["main"]["selected_folder"]:
            self.open_directory(self.userconfig["main"]["selected_folder"])

    def open_directory(self, selected_folder = False):
        if not selected_folder:
            selected_folder = tkinter.filedialog.askdirectory()
        if not selected_folder:
            return False
        self.userconfig["main"]["selected_folder"] = selected_folder
        self.save_config()

        entry = self.nametowidget("directoryselector.directory_entry")
        entry.delete(0,"end")
        entry.insert(0, selected_folder)

        content = get_content(selected_folder, absolute=False)

        operationselector = self.nametowidget("optionselector.operationselector")
        action = operationselector.get_action()
        if action == "clean":
            wordmanager = self.nametowidget("optionselector.wordmanager")
            wordmanager.load_words(content)
        
        before_list = self.nametowidget("comparator_frame.before_frame.before_list")
        after_list = self.nametowidget("comparator_frame.after_frame.after_list")

        before_list.delete(0,'end')
        after_list.delete(0,'end')

        for file in content:
            before_list.insert(tk.END, str(file))
            after_list.insert(tk.END, str(file))