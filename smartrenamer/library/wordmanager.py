#!/usr/bin/env python3

import os
import tkinter as tk
from functools import partial, reduce
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

    def get_action(self):
        return self.action.get()

    def load_words(self, files):
        for child in self.winfo_children():
            child.destroy()

        # String extensions
        filesnoext = []
        for file in files:
            filesnoext.append(str(os.path.splitext(file)[0]).lower())

        # Find substrings
        seqs_ngrams = map(WordManager.allngram, filesnoext)
        counts = Counter(chain.from_iterable(seqs_ngrams))

        # Keep top 50
        highest = {}

        countpa = 0
        for item in counts.most_common():
            substring = item[0]
            count = item[1]

            if not len(substring) > 2:
                continue
            if any(badstring in substring for badstring in [".", "-"]):
                continue

            lowest_key = None
            lowest_count = 0
            if len(highest) > 0:
                lowest_key = min(highest, key=highest.get)
                lowest_count = highest[lowest_key]

            if len(highest) >= 50 and count > lowest_count:
                highest.pop(lowest_key)
                highest[substring] = count
                print(len(highest))
            elif len(highest) < 50:
                highest[substring] = count
                print(len(highest))

        print(len(highest))
        xpos = 0
        ypos = 0
        for substring, count in highest.items():
            # radiobutton = tk.Radiobutton(
            #     self,
            #     text=f"{substring} ({count})",
            #     # variable=self.action,
            #     # value="clean"
            # )
            radiobutton = tk.Checkbutton(
                self,
                text=f"{substring} ({count})",
                # variable=self.operationoptions["autoremove"],
                # onvalue=1, offvalue=0
            )
            radiobutton.grid(column=xpos, row=ypos, sticky="nwe")
            xpos += 1
            if xpos > 9:
                xpos = 0
                ypos += 1
            # radiobutton.pack(side="left")


        # for file in files:
        #     print(file)

    @staticmethod 
    def allngram(seq: str, minn=1, maxn=None) -> Iterator[str]:
        lengths = range(minn, maxn) if maxn else range(minn, len(seq))
        ngrams = map(partial(WordManager.ngram, seq), lengths)
        return set(chain.from_iterable(ngrams))

    @staticmethod
    def ngram(seq: str, n: int) -> Iterator[str]:
        return (seq[i: i+n] for i in range(0, len(seq)-n+1))


    # @staticmethod
    # def allngram(seq: str) -> set:
    #     lengths = range(len(seq))
    #     ngrams = map(partial(WordManager.ngram, seq), lengths)
    #     return set(chain.from_iterable(ngrams))