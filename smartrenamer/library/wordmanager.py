#!/usr/bin/env python3

import math
import json
import re
import os
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

        self.load_components()
    
    def select_all_words(self):
        for word, word_data in self.word_checkboxes.items():
            word_data["checkbox"].select()
    
    def deselect_all_words(self):
        for word, word_data in self.word_checkboxes.items():
            word_data["checkbox"].deselect()
    
    def save_words(self):
        print("In save_words")
        for word, word_data in self.word_checkboxes.items():
            print(f"{word}: {word_data['value'].get()}")
    
    def open_manager_window(self):
        print("In open_manager_window")

    def load_components(self):

        # self.word_container_frame = tk.LabelFrame(self, text="Words", name="word_container_frame", pady=10, padx=10)
        self.word_container_frame = tk.Frame(self, name="word_container_frame", padx=10)

        for i in range(10):
            self.word_container_frame.grid_columnconfigure(i, weight=1)
            if i < 5:
                self.word_container_frame.grid_rowconfigure(i, weight=1)

        # self.action_frame = tk.LabelFrame(self, text="Actions", name="action_frame", pady=10, padx=10)
        self.action_frame = tk.Frame(self, name="action_frame", padx=10)

        buttons = [
            tk.Button(self.action_frame, text='Select all', command= self.select_all_words),
            tk.Button(self.action_frame, text='Deselect all', command= self.deselect_all_words),
            tk.Button(self.action_frame, text='Remove', command= self.save_words),
            tk.Button(self.action_frame, text='Ignore', command= self.save_words),
            tk.Button(self.action_frame, text='Reset', command= self.save_words),
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

        new_from = mainapp.nametowidget("optionselector.operationoptionsselector.unify_separators_from").get()
        new_to = mainapp.nametowidget("optionselector.operationoptionsselector.unify_separators_to").get()

        if (separators_from != new_from or separators_to != new_to) and new_from and new_to:
            mainapp.update_separators(new_from, new_to)
            separators_from, separators_to = new_from, new_to
        return separators_from, separators_to

    def get_action(self):
        return self.action.get()

    def load_words(self, files):
        if self.word_container_frame:
            for child in self.word_container_frame.winfo_children():
                child.destroy()
        self.word_checkboxes = {}
        

        separators_from, separators_to = self.get_separators()
        separators_from_regex = separators_from + separators_to + "()[]{}<>"
        separators_from_regex = '|'.join(map(re.escape, separators_from_regex))

        # print(separators_from_regex)
        # exit()

        file_components = []
        for path in files:
            subcomponents = []
            components = os.path.normpath(path).split(os.sep)
            components[-1] = str(os.path.splitext(components[-1])[0])
            components = [compo.lower() for compo in components]
            for compo in components:
                subcomponents += re.split(separators_from_regex, compo)
            file_components += subcomponents
        
        # print(json.dumps(file_components, indent=4))
        # exit()
        component_counts = dict(Counter(file_components))

        seqs_ngrams = map(WordManager.allngram, file_components)
        counts = dict(Counter(chain.from_iterable(seqs_ngrams)))

        counts.update(component_counts)
        # print(counts)
        # print(len(counts))
        # print(json.dumps(counts, sort_keys=True, indent=4))
        # print(json.dumps(counts, indent=4))
        # exit()

        # Remove bottom 10% of the list and single characters for speed
        # max_key = max(counts, key=counts.get)
        # cutoff = int(counts[max_key] / 10)
        cutoff = 1
        counts = {key:value for key, value in counts.items() if value > cutoff and len(key) > 1 and not key.isnumeric()}
        # print(len(counts))

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
                        # print(f"Removing {sub} because it is in {substring}")
                    if substring in sub:
                        counts.pop(substring, None)
                        # print(f"Removing {substring} because it is in {sub}")
        # print(len(counts))

        top50 = sorted(counts, key=counts.get, reverse=True)[:50]
        # Create top 50 grid
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
            self.word_checkboxes[k]["checkbox"].grid(column=xpos, row=ypos, sticky="nwe")
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

    