#!/usr/bin/env python3

from randomhash import RandomHashFamily
from random import randint
from requests import get
from re import findall

class CountDistinct:
    def __init__(self, k):
        self.k = k
        self.x = [1 for i in range(k)]
        self.rhf = RandomHashFamily(1)
    def onGet(self, a):
        t = self.rhf.hashes(a)[0]
        t = t / (2**32-1)
        # t = (t[randint(0,1)]) / (2^64-1)
        assert(t <= 1)
        if t < self.x[self.k-1] and t not in self.x:
            self.x.append(t)
            self.x.sort()
            self.x = self.x[0:self.k]
    def estimate(self):
        l = sum(map(lambda x: 1 if x == 1 else 0, self.x))
        if l > 0:
            return self.k - l
        else:
            return round((self.k-1)/(self.x[self.k-1])) 


if __name__ == "__main__":
    text = ""
    with open('data/christo.txt') as f:
        for line in f:
            text += line + "\n"
    res = findall(r"\w+", text)
    words = set(res)
    l = len(words)
    print(f"exact size: {l}")
    avgErr = [0 for _ in range(50)]
    for i in range(50):
        est = CountDistinct(400)
        for w in res:
            est.onGet(w)
        v = est.estimate()
        avgErr[i] = abs(l - v) / l
    print(f"average error: {sum(avgErr) / 50}")

