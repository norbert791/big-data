#!/usr/bin/env python3

from random import randint
from requests import get
from random import randint
from re import findall
from math import log2
from randomhash import RandomHashFamily

class CountDistinct:
    def __init__(self, k):
        self.k = k // 2
        self.x = [1 for i in range(k)]
        self.y = [1 for i in range(k)]
        self.rhf = RandomHashFamily(1)
    def onGet(self, a):
        t = self.rhf.hashes(a)[0]
        t = t / (2**32-1)
        # t = (t[randint(0,1)]) / (2^64-1)
        assert(t <= 1)
        lst = self.x if randint(0,1) == 0 else self.y
        if t < lst[self.k-1] and t not in lst:
            lst.append(t)
            lst.sort()
            lst = lst[0:self.k]
    def estimate(self):
        return round((self.k-1)/(self.x[self.k-1])) + round((self.k-1)/(self.y[self.k-1]))


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
        est.onGet(w)
    v = est.estimate()
    print(f"estimated size: {v}")

        
