#!/usr/bin/python
import re

class Corpus:
        
    def __init__(self, corpus_loc=None):
        self.read_corpus(corpus_loc)

    def read_corpus(self, floc):
        if floc:
            f = open(floc)
            s = f.read().split('\n')
            f.close()
            a = map(lambda i: s[i][2:], filter(lambda i: i%2 == 0, range(len(s)))) # get all A lines
            b = map(lambda i: s[i][2:], filter(lambda i: i%2 != 0, range(len(s)))) # get all B lines
            
            self.pairs = zip(a,b)
            self.corpus_loc = floc
        else:
            self.corpus_loc = None
                    
    def do_search(self, search_item):
        if not self.corpus_loc:
            return -1
        else:
            return self.search_pairs(search_item)
        
    def search_pairs(self, word):
        matches = [word]
        for i in range(len(self.pairs)):
            found = re.search(word, self.pairs[i][1])
            
            if found:
                matches.append(self.pairs[i])

        return matches
