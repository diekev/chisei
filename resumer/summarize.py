# encoding=utf8 

from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords
from collections import defaultdict
from string import punctuation
from heapq import nlargest
 
import sys  

reload(sys)  
sys.setdefaultencoding('utf8')


class FrequencySummarizer:
    def __init__(self, min_cut=0.1, max_cut=0.9):
        """
        Initialize the text summarizer.
        Words that have a frequency term lower than min_cut or higher than
        max_cut will be ignored.
        """
        self._min_cut = min_cut
        self._max_cut = max_cut
        self._stopwords = set(stopwords.words('french') + list(punctuation))

    def _compute_frequencies(self, word_sent):
        """
        Compute the frequency of each word.
        Input:
            word_sent: a list of sentences already tokenized.
        Output:
            freq: a dictionary where freq[w] is the frequency of w
        """

        freq = defaultdict(int)

        for s in word_sent:
            for word in s:
                if word not in self._stopwords:
                    freq[word] += 1

        # frequencies normalization and filtering
        m = float(max(freq.values()))

        # using list(freq) instead of freq.keys() since we might change the
        # dictionary's size
        for w in list(freq):
            freq[w] = freq[w] / m

            if freq[w] >= self._max_cut or freq[w] <= self._min_cut:
                del freq[w]

        return freq

    def summarize(self, text, n):
        """
            Return a list of n sentences which represent the summary of the text
        """

        sents = sent_tokenize(text)
        assert n <= len(sents)
        word_sent = [word_tokenize(s.lower()) for s in sents]

        self._freq = self._compute_frequencies(word_sent)
        ranking = defaultdict(int)

        for i, sent in enumerate(word_sent):
            for w in sent:
                if w in self._freq:
                    ranking[i] += self._freq[w]

        sents_idx = self._rank(ranking, n)

        return[sents[j] for j in sents_idx]

    def _rank(self, ranking, n):
        """ return the first n sentences with highest ranking """
        return nlargest(n, ranking, key=ranking.get)

#import urllib3
#import requests
#from bs4 import BeautifulSoup

#http = urllib3.PoolManager()

#def get_only_text(url):
#    page = requests.get(url)
#    soup = BeautifulSoup(page.content, "lxml")
#    text = ' '.join(map(lambda p: p.text, soup.find_all('p')))
#    return soup.title.text, text

#r = requests.get('http://feeds.bbci.co.uk/news/rss.xml')

#feed_xml = r.content

#feed = BeautifulSoup(feed_xml, "lxml")
#to_summarize = map(lambda p: p.text, feed.find_all('guid'))

fs = FrequencySummarizer()
#for article_url in list(to_summarize)[:5]:
#    print (article_url)
#    title, text = get_only_text(article_url)
#    print ('----------------------------------')
#    print (title)
#    for s in fs.summarize(text, 2):
#        print ('*', s)

text = ""

with open('motorstep.txt', 'r') as myfile:
    text = myfile.read().replace('\n', '')

for s in fs.summarize(text, 10):
    print s.encode('utf-8')
