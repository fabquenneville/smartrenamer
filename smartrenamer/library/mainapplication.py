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
                "selected_folder": None,
                "separators_from": ". -_",
                "separators_to": " ",
            }
        }
        self.database = None
        self.directory = None

        self.load_config()
        self.load_components()
        self.load_database()
        if self.userconfig["main"]["selected_folder"]:
            self.set_directory(self.userconfig["main"]["selected_folder"])

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
    
    def get_config(self):
        if not self.userconfig:
            self.load_config()
        return self.userconfig
    
    def update_separators(self, separators_from = None, separators_to = None):
        changed = False
        if separators_from and separators_from != self.userconfig["main"]["separators_from"]:
            self.userconfig["main"]["separators_from"] = separators_from
            changed = True
        if separators_to and separators_to != self.userconfig["main"]["separators_to"]:
            self.userconfig["main"]["separators_to"] = separators_to
            changed = True
        if changed:
            self.save_config()

    def load_config(self):
        config_path = self.get_config_path()
        if os.path.exists(config_path):
            with open(config_path, 'r') as configfile:
                config = json.load(configfile)
                for section_name, section_config in self.userconfig.items():
                    if section_name in config:
                        for config_key, setting in self.userconfig[section_name].items():
                                if config_key in config[section_name]:
                                    self.userconfig[section_name][config_key] = config[section_name][config_key]
            return self.userconfig

    def save_config(self):
        config_path = self.get_config_path(True)
        with open(config_path, 'w') as configfile:
            json.dump(self.userconfig, configfile, indent=4)

    def load_database(self):
        pass

    def load_new_directory(self):
        self.open_new_directory()
        self.load_directory()

    def open_new_directory(self):
        existing_folder = self.userconfig["main"]["selected_folder"]
        if existing_folder:
            return self.set_directory(tkinter.filedialog.askdirectory(initialdir = existing_folder))
        return self.set_directory(tkinter.filedialog.askdirectory())

    def set_directory(self, directory = False):
        if not directory:
            return False
        self.userconfig["main"]["selected_folder"] = directory
        self.save_config()

        entry = self.nametowidget("directoryselector.directory_entry")
        entry.delete(0,"end")
        entry.insert(0, directory)

    def load_directory(self):
        selected_folder = self.userconfig["main"]["selected_folder"]
        if not selected_folder:
            return False


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

