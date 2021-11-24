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
            # padx=10, pady=10,
            *args, **kwargs
        )

        self.action = tk.StringVar()
        self.action_frame = None
        self.managed_word = tk.StringVar()
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
        mainapp = self.winfo_toplevel()
        mainapp.clear_filelists()

        for word, word_data in self.word_checkboxes.items():
            if word_data['value'].get() == 1:
                self.words[word] = {
                    "word": word,
                    "remove" : 1
                }
        
        self.save_words()
        mainapp.load_directory()

    
    def remove_word(self):
        mainapp = self.winfo_toplevel()
        mainapp.clear_filelists()

        self.words[self.managed_word.get()] = {
            "word": self.managed_word.get(),
            "remove" : 1
        }
        self.save_words()
        self.clear_individual_word_entry()
        mainapp.load_directory()
    
    def ignore_words(self):
        mainapp = self.winfo_toplevel()
        mainapp.clear_filelists()

        for word, word_data in self.word_checkboxes.items():
            if word_data['value'].get() == 1:
                self.words[word] = {
                    "word": word,
                    "remove" : 0
                }
        self.save_words()
        mainapp.load_directory()
    
    def ignore_word(self):
        mainapp = self.winfo_toplevel()
        mainapp.clear_filelists()

        self.words[self.managed_word.get()] = {
            "word": self.managed_word.get(),
            "remove" : 0
        }
        self.save_words()
        self.clear_individual_word_entry()

        mainapp.load_directory()
    
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
    
    def clear_individual_word_entry(self):
        word_entry = self.nametowidget("action_frame.individual_word_frame.individual_word_entry")
        word_entry.delete(0,'end')
        word_entry.update()

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
        # Action bar
        self.action_frame = tk.Frame(self, name="action_frame", padx=10)
        components = [
            tk.Button(self.action_frame, text='Select all', command= self.select_all_words),
            tk.Button(self.action_frame, text='Deselect all', command= self.deselect_all_words),
            tk.Button(self.action_frame, text='Remove', command= self.remove_words),
            tk.Button(self.action_frame, text='Ignore', command= self.ignore_words),
            tk.Button(self.action_frame, text='Reset saved words', command= self.reset_words),
            tk.Button(self.action_frame, text='Manage', command= self.open_manager_window),
            tk.LabelFrame(self.action_frame, name="individual_word_frame", text="Add individual word")
        ]
        self.action_frame.grid_rowconfigure(0, weight=1)
        for i in range(len(components)):
            if components[i]._name == "individual_word_frame":
                subcomponents = [
                    tk.Label(
                        components[i],
                        text = "Word:"
                    ),
                    tk.Entry(
                        components[i],
                        name = "individual_word_entry",
                        textvariable = self.managed_word
                    ),
                    tk.Button(components[i], text = 'Remove', command = self.remove_word),
                    tk.Button(components[i], text = 'Ignore', command = self.ignore_word),
                ]
                components[i].grid_rowconfigure(0, weight=1)
                for j in range(len(subcomponents)):
                    subcomponents[j].grid(row = 0, column = j, sticky = "ew")
                    components[i].grid_columnconfigure(j, weight=1)
                # for compo in subcomponents:
                #     compo.pack(side="left")


                components[i].grid(row = 0, column = i, sticky = "ew")
                self.action_frame.grid_columnconfigure(i, weight=2)
            else:
                components[i].grid(row = 0, column = i, sticky = "ew")
                self.action_frame.grid_columnconfigure(i, weight=1)

        # Word grid
        self.word_container_frame = tk.Frame(self, name="word_container_frame", padx=10)
        for i in range(10):
            self.word_container_frame.grid_columnconfigure(i, weight=1)
            if i < 5:
                self.word_container_frame.grid_rowconfigure(i, weight=1)

        self.action_frame.pack(side="top", fill="both", expand=True)
        self.word_container_frame.pack(side="top", fill="both", expand=True)
        # self.individual_word_frame.pack(side="top", fill="both", expand=True)
    
    def get_separators(self):
        mainapp = self.winfo_toplevel()
        config = mainapp.get_config()
        separators_from = config["main"]["separators_from"]
        separators_to = config["main"]["separators_to"]

        new_from = mainapp.nametowidget("options.operationoptionsselector.unify_separators_frame.unify_separators_from").get()
        new_to = mainapp.nametowidget("options.operationoptionsselector.unify_separators_frame.unify_separators_to").get()

        if (separators_from != new_from or separators_to != new_to) and new_from and new_to:
            mainapp.update_separators(new_from, new_to)
            separators_from, separators_to = new_from, new_to
        return separators_from, separators_to
    
    @staticmethod
    def get_all_brackets(format = "tupples"):
        if format == "string":
            return "()[]{}<>"
        elif format == "dict":
            return {
                "parentheses":  ("(", ")"),
                "squares":      ("[", "]"),
                "curly":        ("{", "}"),
                "angles":       ("<", ">"),
            }
        return [
            ("(", ")"),
            ("[", "]"),
            ("{", "}"),
            ("<", ">"),
        ]

    def get_brackets(self):
        mainapp = self.winfo_toplevel()
        bracketname = mainapp.nametowidget("options").get_bracketname()
        inner_bracket = ""
        outter_bracket = ""

        all_brackets = WordManager.get_all_brackets("dict")

        for bname, brackets in all_brackets.items():
            if bracketname == bname:
                inner_bracket = brackets[0]
                outter_bracket = brackets[1]
        
        return inner_bracket, outter_bracket

    def get_action(self):
        return self.action.get()

    def get_removables(self):
        removables = []
        # print(json.dumps(self.words, indent=4))
        # print(json.dumps(self.words.values(), indent=4))
        for word, word_data in self.words.items():
            # print(word_data)
            if word_data["remove"] == 1:
                removables.append(word)
        return removables

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
        # removables = self.get_removables()
        
        separators_from, separators_to = self.get_separators()
        separators_all = separators_from + separators_to + "()[]{}<>"
        separators_from_regex = '|'.join(map(re.escape, separators_all))

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
        # for removable in removables:
        #     counts.pop(removable,)
        
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
                    # subcount = counts.get(sub)
                    # substringcount = counts.get(substring)
                    # if sub in substring and subcount <= substringcount:
                    #     counts.pop(sub, None)
                    # if substring in sub and substringcount <= subcount:
                    #     counts.pop(substring, None)

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

    def clean_filepath_brackets(self, filepath):
        separators_from, separators_to = self.get_separators()
        separators_all = separators_from + separators_to

        inner_bracket, outter_bracket = self.get_brackets()
        brackets = WordManager.get_all_brackets()

        for bracket in brackets:
            if bracket[0] in filepath and bracket[1] in filepath and bracket[0] != inner_bracket and bracket[1] != outter_bracket:
                ib = inner_bracket
                ob = outter_bracket

                ib_pos = filepath.find(bracket[0])
                if ib_pos != 2 and filepath[ib_pos - 1] != os.sep:
                    if filepath[ib_pos - 1] not in separators_all:
                        ib = separators_to + inner_bracket
                
                ob_pos = filepath.find(bracket[1])
                if ob_pos != len(filepath) - 1 and filepath[ib_pos + 1] != os.sep:
                    if filepath[ob_pos + 1] not in separators_all:
                        ob = outter_bracket + separators_to

                filepath = filepath.replace(bracket[0], ib, 1)
                filepath = filepath.replace(bracket[1], ob, 1)
                return self.clean_filepath_brackets(filepath)

        return filepath

    def clean_filepath_separators(self, filepath):
        separators_from, separators_to = self.get_separators()
        separators_all = separators_from + separators_to
        separators_regex = '|'.join(map(re.escape, separators_all))

        components = os.path.normpath(filepath).split(os.sep)
        # Removing file extension
        components[-1] = str(os.path.splitext(components[-1])[0])
        
        new_components = []
        for compo in components:
            subcomponents = []
            subcomponents += re.split(separators_regex, compo)
            new_compo = separators_to.join(subcomponents)
            new_components.append(new_compo)
        
        tmp_filepath = os.path.join(*new_components)

        # Removing double, heading and trailing separators
        new_filepath = ""
        last_positive = False
        for i in range(len(tmp_filepath)):
            if tmp_filepath[i] == separators_to:
                if last_positive:
                    continue
                last_positive = True
                if i == 0:
                    continue
            else:
                last_positive = False
            new_filepath += tmp_filepath[i]
        new_filepath = WordManager.remove_trail_char(separators_to, new_filepath)
        
        # Adding back extension
        new_filepath = "." + os.sep + new_filepath + str(os.path.splitext(filepath)[-1])
        return new_filepath
    
    @staticmethod
    def remove_trail_char(character, string):
        if string[-1] == character:
            return WordManager.remove_trail_char(character, string[:-1])
        return string

    def clean_filepath_autoremove(self, filepath):
        separators_from, separators_to = self.get_separators()
        brackets = WordManager.get_all_brackets("string")
        separators_all = separators_from + separators_to + brackets
        removables = self.get_removables()
        
        components = os.path.normpath(filepath).split(os.sep)
        # Removing file extension
        components[-1] = str(os.path.splitext(components[-1])[0])

        new_components = ["." + os.sep, ]
        for compo in components:
            separator_positions = {}
            for separator in separators_all:
                separator_positions[separator] = []
            
            for i in range(len(compo)):
                if compo[i] in separators_all:
                    separator_positions[compo[i]].append(i)
            
            all_pos = []
            for matches in separator_positions.values():
                all_pos += matches
            all_pos.append(len(compo))
            all_pos = sorted(all_pos)
            
            start = 0
            new_compo = ""
            skip_next = False
            for i in range(len(all_pos)):
                if skip_next:
                    skip_next = False
                    continue
                if i >= len(all_pos):
                    break
                separator_before = None
                end = all_pos[i]
                word = compo[start:end]
                separator_after = None

                if start != 0:
                    separator_before = compo[start - 1]

                if end < len(compo):
                    separator_after = compo[end]
                
                if start == end and separator_before:
                    new_compo += separator_before

                elif word.lower() not in removables:
                    if separator_before:
                        new_compo += separator_before
                    new_compo += word

                if word.lower() in removables and separator_before and separator_after and separator_before in brackets and separator_after in brackets:
                    start = end + 2
                    skip_next = True
                else:
                    start = end + 1
            
            new_components.append(new_compo)

        new_components[-1] += str(os.path.splitext(filepath)[-1])
        return os.path.join(*new_components)

    def clean_filepath(self, filepath):
        mainapp = self.winfo_toplevel()
        options = mainapp.nametowidget("options")
        operationoptions = options.get_operationoptions()
        config = mainapp.get_config()

        # print(get_operationoptions)
        # print(json.dumps(get_operationoptions, indent=4))
        # exit()
        # print(f"Original: {filepath}")
        if operationoptions["unify_brackets"] == 1:
            filepath = self.clean_filepath_brackets(filepath)
        # print(f"after clean_filepath_brackets: {filepath}")
        if operationoptions["unify_separators"] == 1:
            filepath = self.clean_filepath_separators(filepath)
        # print(f"after clean_filepath_separators: {filepath}")
        if operationoptions["autoremove"] == 1:
            filepath = self.clean_filepath_autoremove(filepath)
        # print(f"after clean_filepath_autoremove: {filepath}")
        return filepath
