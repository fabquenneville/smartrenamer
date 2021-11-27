#!/usr/bin/env python3

import json
import os
import sqlite3
from pathlib import Path
import tkinter as tk

from .comparator import Comparator
from .mainmenu import MainMenu
from .options import Options
from .wordmanager import WordManager
from .tools import get_content

class MainApplication(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        self.colors = None
        self.mainmenu = None
        self.options = None
        self.comparator = None
        self.userconfig = {
            "main": {
                "selected_folder": None,
                "separators_from": WordManager.get_all_brackets(format="string"),
                "separators_to": " ",
            }
        }
        self.database = None

        self.load_config()
        self.load_components()
        self.load_database()

        if self.userconfig["main"]["selected_folder"]:
            self.options.set_directory(self.userconfig["main"]["selected_folder"])
            self.options.load_directory()

    def load_components(self):
        self.title("smartrenamer")
        w, h = self.winfo_screenwidth(), self.winfo_screenheight()
        self.geometry("%dx%d+0+0" % (w, h))
        self.options = Options(self)
        self.options.pack(fill="x")

        self.mainmenu = MainMenu(self)
        self.comparator = Comparator(self)

        self.comparator.pack(expand=True, fill="both")

        self.config(menu=self.mainmenu)

    @staticmethod
    def get_config_path(createfolders = False):
        homepath = str(Path.home())
        if not homepath[-1] == os.sep:
            homepath += os.sep
        config_folder_path = os.path.join(homepath, ".config")
        app_config_folder_path = os.path.join(config_folder_path, "smartrenamer")
        app_config_path = os.path.join(app_config_folder_path, "config.json")

        if not os.path.isdir(config_folder_path) and createfolders:
            os.mkdir(config_folder_path)
        
        if not os.path.isdir(app_config_folder_path) and createfolders:
            os.mkdir(app_config_folder_path)
        
        return app_config_path

    @staticmethod
    def get_database_path(createfolders = False):
        homepath = str(Path.home())
        if not homepath[-1] == os.sep:
            homepath += os.sep
        config_folder_path = os.path.join(homepath, ".config")
        app_config_folder_path = os.path.join(config_folder_path, "smartrenamer")
        app_database_path = os.path.join(app_config_folder_path, "smartrenamer.sqlite3")

        if not os.path.isdir(config_folder_path) and createfolders:
            os.mkdir(config_folder_path)
        
        if not os.path.isdir(app_config_folder_path) and createfolders:
            os.mkdir(app_config_folder_path)
        
        return app_database_path
    
    def get_config(self):
        if not self.userconfig:
            self.load_config()
        return self.userconfig

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

    def save_config_directory(self, directory):
        if not directory:
            return False
        self.userconfig["main"]["selected_folder"] = directory
        self.save_config()

    def save_config(self):
        config_path = self.get_config_path(True)
        with open(config_path, 'w') as configfile:
            json.dump(self.userconfig, configfile, indent=4)
    
    def get_dbcon(self):
        if not self.database:
            self.load_database()
        return self.database

    def load_database(self):
        db_path = self.get_database_path(True)
        self.database  = sqlite3.connect(db_path, detect_types = sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES)
        self.database.row_factory = sqlite3.Row
        # self.create_tables()
    
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

    def get_files_list(self):
        selected_folder = self.userconfig["main"]["selected_folder"]
        if not selected_folder:
            return False

        return get_content(selected_folder, absolute=False)

    def clear_filelists(self):
        before_list = self.nametowidget("comparator_frame.before_frame.before_list")
        after_list = self.nametowidget("comparator_frame.after_frame.after_list")
        before_list.delete(0,'end')
        after_list.delete(0,'end')
        before_list.update()
        after_list.update()

    def get_separators_all(self):
        separators = ""

        for separator in self.userconfig["main"]["separators_from"]:
            if separator not in separators:
                separators += separator

        for separator in self.userconfig["main"]["separators_to"]:
            if separator not in separators:
                separators += separator
        
        return separators


        