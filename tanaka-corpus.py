#!/usr/bin/python

import sys, re, pygtk
pygtk.require('2.0')
import gtk

class Corpus:
        
    def __init__(self, corpus_loc=None):
        print 'no'    

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
                
    
    def do_search(self, widget, event, data=None):
        if not self.corpus_loc:
            self.no_dict_dialog()
        else:
            search_string = self.entry.get_text()
            self.results = self.search_pairs(search_string)
            self.update_liststore(self.results, search_string)
        
    def search_pairs(self, word):
        matches = []
        for i in range(len(self.pairs)):
            found = re.search(word, self.pairs[i][1])
            
            if found:
                matches.append(self.pairs[i])

        self.status.push(1, 'Found %d sentences containing "%s".'%(len(matches), word))

        return matches
