#!/usr/bin/env python3

import math
import json
import re
import os
import sqlite3
import tkinter as tk
from functools import partial
from itertools import chain
from typing import Iterator
from collections import Counter


class WordManager(tk.LabelFrame):
    def __init__(self, parent, *args, **kwargs):
        tk.LabelFrame.__init__(
            self, parent,
            text="Word manager",
            name="wordmanager",
            padx=10, pady=10,
            *args, **kwargs
        )

        self.action = tk.StringVar()
        self.action_frame = None
        self.word_container_frame = None
        self.word_checkboxes = {}
        self.words = {}
        
        self.load_db_words()
        self.load_components()
    
    def select_all_words(self):
        for word, word_data in self.word_checkboxes.items():
            word_data["checkbox"].select()
    
    def deselect_all_words(self):
        for word, word_data in self.word_checkboxes.items():
            word_data["checkbox"].deselect()
    
    def remove_words(self):
        for word, word_data in self.word_checkboxes.items():
            if word_data['value'].get() == 1:
                self.words[word] = {
                    "word": word,
                    "remove" : 1
                }
        self.save_words()
        self.load_words()
    
    def ignore_words(self):
        for word, word_data in self.word_checkboxes.items():
            if word_data['value'].get() == 1:
                self.words[word] = {
                    "word": word,
                    "remove" : 0
                }
        self.save_words()
        self.load_words()
    
    def save_words(self):
        mainapp = self.winfo_toplevel()
        sqlite = mainapp.get_dbcon()
        cursor = sqlite.cursor()
        if not self.test_tables():
            self.create_tables()

        cursor.execute('DELETE FROM words;')
        for word, word_data in self.words.items():
            cursor = sqlite.cursor()
            sql = ''' INSERT OR IGNORE INTO words(word,remove)
                    VALUES(?,?) '''
            cursor.execute(sql, list(word_data.values()))
        sqlite.commit()

    def reset_words(self, verbose = False):
        mainapp = self.winfo_toplevel()
        sqlite = mainapp.get_dbcon()
        cursor = sqlite.cursor()
        if not self.test_tables():
            self.create_tables()

        cursor.execute('DELETE FROM words;')
        if verbose:
            print(f"Deleted {cursor.rowcount()} from sqlite")
        
        sqlite.commit()
    
    def open_manager_window(self):
        print("In open_manager_window")

    def load_components(self):
        self.word_container_frame = tk.Frame(self, name="word_container_frame", padx=10)

        for i in range(10):
            self.word_container_frame.grid_columnconfigure(i, weight=1)
            if i < 5:
                self.word_container_frame.grid_rowconfigure(i, weight=1)

        self.action_frame = tk.Frame(self, name="action_frame", padx=10)

        buttons = [
            tk.Button(self.action_frame, text='Select all', command= self.select_all_words),
            tk.Button(self.action_frame, text='Deselect all', command= self.deselect_all_words),
            tk.Button(self.action_frame, text='Remove', command= self.remove_words),
            tk.Button(self.action_frame, text='Ignore', command= self.ignore_words),
            tk.Button(self.action_frame, text='Reset saved words', command= self.reset_words),
            tk.Button(self.action_frame, text='Manage', command= self.open_manager_window)
        ]

        self.action_frame.pack(side="top", fill="both", expand=True)

        self.action_frame.grid_rowconfigure(0, weight=1)
        for i in range(len(buttons)):
            buttons[i].grid(row = 0, column = i, sticky = "ew")
            self.action_frame.grid_columnconfigure(i, weight=1)

        self.word_container_frame.pack(side="left", fill="both", expand=True)
    
    def get_separators(self):
        mainapp = self.winfo_toplevel()
        config = mainapp.get_config()
        separators_from = config["main"]["separators_from"]
        separators_to = config["main"]["separators_to"]

        new_from = mainapp.nametowidget("options.operationoptionsselector.unify_separators_from").get()
        new_to = mainapp.nametowidget("options.operationoptionsselector.unify_separators_to").get()

        if (separators_from != new_from or separators_to != new_to) and new_from and new_to:
            mainapp.update_separators(new_from, new_to)
            separators_from, separators_to = new_from, new_to
        return separators_from, separators_to
    
    def get_brackets(self):
        mainapp = self.winfo_toplevel()
        bracketname = mainapp.nametowidget("options").get_bracketname()
        inner_bracket = ""
        outter_bracket = ""

        if bracketname == "parentheses":
            inner_bracket = "("
            outter_bracket = ")"
        elif bracketname == "squares":
            inner_bracket = "["
            outter_bracket = "]"
        elif bracketname == "curly":
            inner_bracket = "{"
            outter_bracket = "}"
        elif bracketname == "angles":
            inner_bracket = "<"
            outter_bracket = ">"
        
        return inner_bracket, outter_bracket

    def get_action(self):
        return self.action.get()

    def load_db_words(self):
        mainapp = self.winfo_toplevel()
        sqlite = mainapp.get_dbcon()
        cursor = sqlite.cursor()

        cursor.execute("SELECT * FROM words")
        words = cursor.fetchall()

        for word in words:
            self.words[word["word"]] = dict(word)
        
    def load_words(self):
        mainapp = self.winfo_toplevel()
        if self.word_container_frame:
            for child in self.word_container_frame.winfo_children():
                child.destroy()
        self.word_checkboxes = {}
        
        separators_from, separators_to = self.get_separators()
        separators_from_regex = separators_from + separators_to + "()[]{}<>"
        separators_from_regex = '|'.join(map(re.escape, separators_from_regex))

        file_components = []
        files = mainapp.get_files_list()
        for path in files:
            subcomponents = []
            components = os.path.normpath(path).split(os.sep)
            components[-1] = str(os.path.splitext(components[-1])[0])
            components = [compo.lower() for compo in components]
            for compo in components:
                subcomponents += re.split(separators_from_regex, compo)
            file_components += subcomponents
        
        component_counts = dict(Counter(file_components))

        seqs_ngrams = map(WordManager.allngram, file_components)
        counts = dict(Counter(chain.from_iterable(seqs_ngrams)))

        counts.update(component_counts)
        
        cutoff = 1
        counts = {key:value for key, value in counts.items() if value > cutoff and len(key) > 1 and not key.isnumeric()}

        # Remove substrings of substrings
        substrings = sorted(list(counts.keys()), key=len, reverse=True)
        for substring in substrings:
            if substring not in counts:
                continue
            all_remaining_substrings = list(counts.keys())
            for sub in all_remaining_substrings:
                if sub != substring:
                    if sub in substring:
                        counts.pop(sub, None)
                    if substring in sub:
                        counts.pop(substring, None)

        for word in self.words.keys():
            counts.pop(word, None)

        # Create top 50 grid
        top50 = sorted(counts, key=counts.get, reverse=True)[:50]

        xpos = 0
        ypos = 0
        for k in top50:
            if ypos > 4:
                break

            self.word_checkboxes[k] = {
                "word": k,
                "checkbox": None,
                "value": tk.IntVar()
            }
            self.word_checkboxes[k]["checkbox"] = tk.Checkbutton(
                self.word_container_frame,
                text=f"{k} ({counts[k]})",
                variable = self.word_checkboxes[k]["value"],
                onvalue = 1, offvalue = 0
            )

            self.word_checkboxes[k]["checkbox"].grid(column=xpos, row=ypos, sticky="nw")
            xpos += 1
            if xpos > 9:
                xpos = 0
                ypos += 1

    @staticmethod 
    def allngram(seq: str, minn=1, maxn=None) -> Iterator[str]:
        lengths = range(minn, maxn) if maxn else range(minn, len(seq))
        ngrams = map(partial(WordManager.ngram, seq), lengths)
        return set(chain.from_iterable(ngrams))

    @staticmethod
    def ngram(seq: str, n: int) -> Iterator[str]:
        return (seq[i: i+n] for i in range(0, len(seq)-n+1))

    def create_tables(self):
        mainapp = self.winfo_toplevel()
        sqlite = mainapp.get_dbcon()
        cursor = sqlite.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS words (
                word TEXT NOT NULL PRIMARY KEY,
                remove INTEGER NOT NULL DEFAULT 0
            )
        ''')
        sqlite.commit()

    def drop_tables(self):
        mainapp = self.winfo_toplevel()
        sqlite = mainapp.get_dbcon()
        cursor = sqlite.cursor()
        cursor.execute('''
            DROP TABLE IF EXISTS words
        ''')
        sqlite.commit()

    def test_tables(self):
        mainapp = self.winfo_toplevel()
        sqlite = mainapp.get_dbcon()
        cursor = sqlite.cursor()
        cursor.execute('''
            SELECT name FROM sqlite_master WHERE type='table' AND name='words';
        ''')
        if (cursor.fetchone()):
            return True
        return False

    def clean_filename(self, original_filename):
        new_filename = original_filename

        separators_from, separators_to = self.get_separators()
        separators_all = separators_from + separators_to

        inner_bracket, outter_bracket = self.get_brackets()
        brackets = [
            ("(", ")"),
            ("[", "]"),
            ("{", "}"),
            ("<", ">"),
        ]
        for bracket in brackets:
            if bracket[0] in original_filename and bracket[1] in original_filename and bracket[0] != inner_bracket and bracket[1] != outter_bracket:
                ib = inner_bracket
                ob = outter_bracket

                ib_pos = new_filename.find(bracket[0])
                if ib_pos != 2 and new_filename[ib_pos - 1] != os.sep:
                    if new_filename[ib_pos - 1] not in separators_all:
                        ib = separators_to + inner_bracket
                
                ob_pos = new_filename.find(bracket[1])
                if ob_pos != len(new_filename) - 1 and new_filename[ib_pos + 1] != os.sep:
                    if new_filename[ob_pos + 1] not in separators_all:
                        ob = outter_bracket + separators_to

                new_filename = new_filename.replace(bracket[0], ib, 1)
                new_filename = new_filename.replace(bracket[1], ob, 1)
                return self.clean_filename(new_filename)

        return new_filename