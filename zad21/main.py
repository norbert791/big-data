#!/usr/bin/env python3

from random import randint
from requests import get
from random import randint
from re import findall
from math import log2


class CountDistinct():
    def __init__(self, k):
        self.k = k
        self.l = [0,0]
    def onTick(self):
        c = randint(0,1)
        if c == 0:
            self.l[randint(0,1)] += 1
    def onTickChained(self):
        for _ in range(self.k):
            self.onTick()
    def onGet(self):
        return sum(self.l)


if __name__ == "__main__":
    url = "https://www.gutenberg.org/cache/epub/1184/pg1184.txt"
    monteChristo = get(url)
    body = monteChristo.text
    res = findall(r"\w+", body)
    words = set(res)
    l = len(words)
    print(f"exact size: {l}")
    est = CountDistinct(400)
    for w in words:
        est.onTick()
    v = est.onGet()
    print(f"estimated size: {v}")

        
