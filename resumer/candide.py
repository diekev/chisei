#!/usr/bin/env python
# -*- coding: utf8  -*-

from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords
from collections import defaultdict
from string import punctuation
from heapq import nlargest
import sys
import json

reload(sys)  
sys.setdefaultencoding('utf8')

def compute_occurences(sentences, stopwords):
    """
    Compute the occurence of each word.
    Input:
        sentences: a list of sentences already tokenized.
    Output:
        occurences: a dictionary where occurences[word] is the occurence of word
    """
    occurences = defaultdict(int)

    for sentence in sentences:
        for word in sentence:
            if word not in stopwords:
                occurences[word] += 1

    return occurences

def normalize_occurences(occurences):
    m = float(max(occurences.values()))

    for w in occurences.keys():
        occurences[w] = occurences[w] / m

def normalize_occurences_bounded(occurences, min_bound, max_bound):
    m = float(max(frequencies.values()))

    # using list(occurences) instead of occurences.keys() since we
    # might change the dictionary's size
    for w in list(occurences):
        occurences[w] = occurences[w] / m

        if occurences[w] >= min_bound or occurences[w] <= max_bound:
            del occurences[w]


class FrequencySummarizer:
    def __init__(self, min_cut=0.1, max_cut=0.9):
        """
        Initialize the text summarizer.
        Words that have a frequency term lower than min_cut or higher than
        max_cut will be ignored.
        """
        self._min_cut = min_cut
        self._max_cut = max_cut
        self._stopwords = set(stopwords.words('english') + list(punctuation))
        self._freq = defaultdict(int)

    # Compute the frequency of each word in the given text.
    def analyse_frequencies(self, text):
        tmp_sentences = sent_tokenize(text)
        sentences = [word_tokenize(s.lower()) for s in tmp_sentences]

        self._training_freq = compute_occurences(sentences, self._stopwords)

        print("Training entries: {0}".format(len(self._training_freq)))

        #for k, v in self._freq.items():
        #    print("Word: {0}, frequency: {1}".format(k, v))

    # Merge the training frequencies with the stored ones.
    def finalize_training(self):
        for k, v in self._training_freq.items():
            if k in self._freq:
                self._freq[k] += v
            else:
                self._freq[k] = v

        print("Entries: {0}".format(len(self._freq)))

    # Read frequencies dictionary from JSON file
    def read_frequencies(self, path):
        with open(path, 'r') as f:
            try:
                self._freq = json.load(f)
            except ValueError:
                self._freq = {}

        print("Loaded entries: {0}".format(len(self._freq)))

    # Write frequencies dictionary to JSON file
    def write_frequencies(self, path):
        with open(path, 'w') as f:
            json.dump(self._freq, f)

    # Rating is done by multiplying together the probabilities that each word
    # has to be of the given class. This per word probability is computed as
    # the occurence of the word divided by the total number of words in the
    # class dictionary.
    def rate(self, text):
        tmp_sentences = sent_tokenize(text)
        sentences = [word_tokenize(s.lower()) for s in tmp_sentences]

        # Compute the total number of occurences
        count = 0

        for k, v in self._freq.items():
            count += v

        # Laplace smoothing: to avoit multiply by zero in case the word is not
        # in the dictionary we add one to both the numerator and denominator.
        # In the latter case, this implies adding the size of the dictionary
        # since we add one per item in it.
        count += len(self._freq)
        print("Count: {}".format(count))
        not_in_dict_weight = 1 / count
        print("Smoothing term: {}".format(not_in_dict_weight))

        rating = 0.0

        for sentence in sentences:
            for word in sentence:
                if word in self._stopwords:
                    continue

                if word in self._freq:
                    tmp = (self._freq[word] + 1) / (count)

                    #if tmp == 0.0:
                        #print("tmp is zero!")

                    rating += tmp
                else:
                    #print("Word {} not in dict!".format(word))
                    rating += not_in_dict_weight

        print("Text rating: {}".format(rating))


def main():
    if len(sys.argv) == 1:
        print("Need to pass a string as argument")

    text = ""

    with open(sys.argv[1], 'r') as input_file:
        text = input_file.read()

    fs = FrequencySummarizer()
    fs.read_frequencies("frequencies.json")

    # Training.
    #fs.analyse_frequencies(text)
    #fs.finalize_training()

    fs.rate(text)

    #fs.write_frequencies("frequencies.json")


if __name__ == "__main__":
    main()
