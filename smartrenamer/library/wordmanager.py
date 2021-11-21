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

        for i in range(10):
            self.grid_columnconfigure(i, weight=1)
            if i < 5:
                self.grid_rowconfigure(i, weight=1)

        self.action = tk.StringVar()
    
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
        for child in self.winfo_children():
            child.destroy()

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
            radiobutton = tk.Checkbutton(
                self,
                text=f"{k} ({counts[k]})"
            )
            radiobutton.grid(column=xpos, row=ypos, sticky="nwe")
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

    