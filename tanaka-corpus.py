#!/usr/bin/python

import sys, re

class Corpus:
    
    def __init__(self, corpus_loc):
        f = open(corpus_loc)
        s = f.read().split('\n')
        f.close()
        a = map(lambda i: s[i][2:], filter(lambda i: i%2 == 0, range(len(s)))) # get all A lines
        b = map(lambda i: s[i][2:], filter(lambda i: i%2 != 0, range(len(s)))) # get all B lines
        
        self.pairs = zip(a,b)

        self.search_loop()

    def search_loop(self):
        in_str = ''
        while (in_str != 'exit'):
            in_str = raw_input('Enter search term\n')
            results = self.search_pairs(in_str)

    def search_pairs(self, word):
        matches = []
        for i in range(len(self.pairs)):
            found = re.search(word, self.pairs[i][1])
            
            if found:
                matches.append(self.pairs[i])

        for item in matches:
            print item[0]
        
        print 'Found %d sentences containing "%s".'%(len(matches), word)

if __name__ == '__main__':
    if not sys.argv:
        print 'Provide location of corpus file.'
        sys.exit(1)
    else:
        Corpus(sys.argv[1])
