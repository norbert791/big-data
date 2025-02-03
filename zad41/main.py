#!/usr/bin/env python3

from mmh3 import hash
from random import randint
import os
from sklearn.cluster import KMeans
from sklearn.datasets import fetch_20newsgroups
import matplotlib.pyplot as plt
from sklearn.feature_extraction.text import CountVectorizer

def new_hash_family(n: int):
    temp = [randint(0, 2**32 - 1) for _ in range(n)]
    return [lambda x: hash(str(x), seed=temp[i]) for i in range(n)]

def new_similarity(n: int):
    family = new_hash_family(n)
    return lambda x, y: sum([1 for h in family if h(x) == h(y)]) / n

def preprocess_documents(documents):
    vectorizer = CountVectorizer(stop_words='english')
    X = vectorizer.fit_transform(documents)
    arr = X.toarray()
    features = vectorizer.get_feature_names_out()
    raw = [[features[i] for i in range(len(features)) if arr[j][i] > 0] for j in range(len(arr))]
    raw = [' '.join(x) for x in raw]
    return raw

def main():
    # Use fetch_20newsgroups as a collection of documents
    newsgroups = fetch_20newsgroups(subset='all')
    data_points = newsgroups.data[:100]  # Take a subset of 100 documents
    filenames = newsgroups.filenames[:100]  # Corresponding filenames
    
    # Preprocess the documents
    word_matrix = preprocess_documents(data_points)
    print(word_matrix[0])
    
    # Perform K-means clustering
    n_clusters = 5
    similarity = new_similarity(100)
    similarity_matrix = [[similarity(x, y) for y in word_matrix] for x in word_matrix]
    
    kmeans = KMeans(n_clusters=n_clusters, random_state=0).fit(similarity_matrix)
    labels = kmeans.labels_
    
    # Enumerate clusters and their members
    clusters = {i: [] for i in range(n_clusters)}
    for idx, label in enumerate(labels):
        clusters[label].append(idx)
    
    for cluster, members in clusters.items():
        print(f"Cluster {cluster}:")
        mean_similarity = sum([similarity_matrix[i][j] for i in members for j in members]) / (len(members) ** 2)
        print(f"  Mean Similarity: {mean_similarity:.2f}")
        for member in members:
            print(f"  Document: {filenames[member]}")

if __name__ == '__main__':
    main()