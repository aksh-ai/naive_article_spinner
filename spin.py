import nltk
import random
import numpy as np 
from bs4 import BeautifulSoup
from future.utils import iteritems

def sample(d):
    r = random.random()
    cummulative = 0
    for w, p in iteritems(d):
        cummulative += p
        if r<cummulative:
            return w 

def spin():
    review = random.choice(positive_reviews)
    s = review.text.lower()
    print(f"Original:\n{s}")
    tokens = nltk.tokenize.word_tokenize(s)
    for i in range(len(tokens) - 2):
        k = (tokens[i], tokens[i+2])
        if k in trigram_probabilities:
            w = sample(trigram_probabilities[k])
            tokens[i+1] = w
    print("Spun: \n")
    print(" ".join(tokens).replace(" .", ".").replace(" '", "'").replace(" ,", ",").replace("$ ", "$").replace(" !", "!"))
    print()

positive_reviews = BeautifulSoup(open('dataset/positive.review').read())
positive_reviews = positive_reviews.findAll('review_text')

trigram = dict()

for review in positive_reviews:
    s = review.text.lower()
    tokens = nltk.tokenize.word_tokenize(s)
    for i in range(len(tokens) - 2):
        k = (tokens[i], tokens[i+2])
        if k not in trigram:
            trigram[k] = []
        trigram[k].append(tokens[i+1])

trigram_probabilities = {}

for k, words in iteritems(trigram):
    if len(set(words)) > 1:
        d = {}
        n = 0
        for w in words:
            if w not in d:
                d[w] = 0
            d[w] += 1
            n += 1 
        for w, c in iteritems(d):
            d[w] = float(c)/n
        trigram_probabilities[k] = d         

spin()