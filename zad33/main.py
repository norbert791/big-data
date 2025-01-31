import hashlib
import numpy as np
import re

class CountMinSketch:
    def __init__(self, width, depth, prime=2**31-1):
        self.width = width
        self.depth = depth
        self.prime = prime
        self.table = np.zeros((depth, width), dtype=int)
        self.hash_functions = [self._generate_hash_function() for _ in range(depth)]

    def _generate_hash_function(self):
        a = np.random.randint(1, self.prime - 1)
        b = np.random.randint(0, self.prime - 1)
        return lambda x: (a * int(hashlib.md5(str(x).encode()).hexdigest(), 16) + b) % self.prime % self.width

    def add(self, item):
        for i, hash_function in enumerate(self.hash_functions):
            index = hash_function(item)
            self.table[i][index] += 1

    def count(self, item):
        min_count = float('inf')
        for i, hash_function in enumerate(self.hash_functions):
            index = hash_function(item)
            min_count = min(min_count, self.table[i][index])
        return min_count

# Example usage
if __name__ == "__main__":
    def preprocess(text):
        text = text.lower()
        text = re.sub(r'[^a-z\s]', '', text)
        words = text.split()
        return words

    def load_file(filepath):
        with open(filepath, 'r') as file:
            return file.read()

    # Load and preprocess the text
    text = load_file('zad33/hamlet.txt')
    words = preprocess(text)

    # Initialize CountMinSketch and a set for exact counts
    cms = CountMinSketch(width=2000, depth=10)
    exact_counts = {}

    # Count words using both CountMinSketch and exact counts
    for word in words:
        cms.add(word)
        if word in exact_counts:
            exact_counts[word] += 1
        else:
            exact_counts[word] = 1

    # Compute mean relative error
    total_error = 0
    for word, exact_count in exact_counts.items():
        cms_count = cms.count(word)
        total_error += abs(cms_count - exact_count) / exact_count

    mean_relative_error = total_error / len(exact_counts)
    print(f"Mean Relative Error: {mean_relative_error}")