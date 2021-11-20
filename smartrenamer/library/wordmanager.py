#!/usr/bin/env python3

import os
import time
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
        counts = dict(Counter(chain.from_iterable(seqs_ngrams)))
        max_key = max(counts, key=counts.get)
        cutoff = int(counts[max_key] / 10)
        counts = {key:value for key, value in counts.items() if value > cutoff and len(key) > 1}

        # # keep top 20%
        # listlist = sorted(list(counts.values()), reverse=True)
        # for i in listlist:
        #     print(i)
        # # print()
        # exit()
        # qtr = sorted(list(counts.values()), reverse=True)[int(len(counts) / 4)]
        # print(qtr)

        # print("Here")
        start_time = time.time()

        # print(len(counts))
        # exit()

        # keepers = {}
        # existing_keys = []

        substrings = sorted(list(counts.keys()), key=len, reverse=True)


        for substring in substrings:
            # print(len(counts))
            # print("--- %s seconds ---" % (time.time() - start_time))
            if substring not in counts:
                continue
            # if counts[substring] < 1:
            #     counts.pop(substring)
            #     continue
            # if len(substring) < 2:
            #     counts.pop(substring)
            #     continue
            all_remaining_substrings = list(counts.keys())
            # submatch = False
            for sub in all_remaining_substrings:
                if sub != substring:
                    if sub in substring:
                        counts.pop(sub, None)
                    if substring in sub:
                        counts.pop(substring, None)
                        # submatch = True
                        # break
            # if submatch:
            #     counts.pop(substring)
            #     continue

            
            # if 



        # counts = dict(counts)
        # counts = {key:value for key, value in counts.items() if value > 1 and len(key) > 1}
        # substrings = list(counts.keys())
        # unique_substrings = WordManager.substringSieve(list(counts.keys()))
        # unique_substrings = WordManager.string_set(substrings)
        # unique_substrings = WordManager.filtered_substrings(substrings)
        # print("--- %s seconds ---" % (time.time() - start_time))
        # print("There")


        # print(len(counts))
        # print(len(unique_substrings))
        # exit()
        # print(len(list(counts)))
        # print(len(counts))
        # Keep top 50
        # highest = {}

        # countpa = 0
        # for item in counts.most_common():
        #     highest_keys = highest.keys
        #     highest_values = highest.values
        #     substring = item[0]
        #     count = item[1]

        #     if not len(substring) > 2:
        #         continue
        #     if any(badstring in substring for badstring in [".", "-"]):
        #         continue

        #     lowest_key = None
        #     lowest_count = 0
        #     if len(highest) > 0:
        #         lowest_key = min(highest, key=highest.get)
        #         lowest_count = highest[lowest_key]


        #     if len(highest) >= 50 and count > lowest_count:
        #         highest.pop(lowest_key)
        #         highest[substring] = count
        #     elif len(highest) < 50:
        #         highest[substring] = count

        xpos = 0
        ypos = 0
        for substring, count in counts.items():
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
    # def filtered_substrings(string_list):
    #     return list(filter(lambda x: [x for i in string_list if x in i and x != i] == [], string_list))

    # @staticmethod
    # def string_set(string_list):
    #     return set(i for i in string_list if not any(i in s for s in string_list if i != s))
    
    # @staticmethod
    # def allngram(seq: str) -> set:
    #     lengths = range(len(seq))
    #     ngrams = map(partial(WordManager.ngram, seq), lengths)
    #     return set(chain.from_iterable(ngrams))

    # @staticmethod
    # def substringSieve(string_list):
    #     string_list.sort(key=lambda s: len(s), reverse=True)
    #     out = []
    #     for s in string_list:
    #         if not any([s in o for o in out]):
    #             out.append(s)
    #     return out

    