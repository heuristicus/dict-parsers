#!/usr/bin/python

import sys, re, pygtk
pygtk.require('2.0')
import gtk

class Corpus:
    
    
    
    def __init__(self, corpus_loc):
        f = open(corpus_loc)
        s = f.read().split('\n')
        f.close()
        a = map(lambda i: s[i][2:], filter(lambda i: i%2 == 0, range(len(s)))) # get all A lines
        b = map(lambda i: s[i][2:], filter(lambda i: i%2 != 0, range(len(s)))) # get all B lines
        
        self.pairs = zip(a,b)

        self.window = gtk.Window(gtk.WINDOW_TOPLEVEL)
        self.window.set_title('corpus_search')
        self.window.set_position(gtk.WIN_POS_CENTER)
        self.window.set_size_request(500, 500)
        self.window.connect('destroy', gtk.main_quit)

        self.make_gui_widgets()
        
        v1 = gtk.HBox()
        v1.pack_start(self.search_btn, False, False, 0)
        v1.pack_start(self.entry)
        
        scr_win = gtk.ScrolledWindow()
        scr_win.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
        scr_win.add_with_viewport(self.treeview)

        v3 = gtk.VBox()
        v3.pack_start(scr_win, True, True, 0)
        v3.pack_end(v1, False, False,0)

        self.window.add(v3)
        self.window.set_focus(self.entry)
        self.window.show_all()

    def make_gui_widgets(self):
        self.create_entry()
        self.create_buttons()
        self.create_treeview()
        
    def create_entry(self):
        self.entry = gtk.Entry()
        self.entry.set_visibility(True)
        self.entry.connect('key-press-event', self.do_search, 'entry')
        
    def create_buttons(self):
        self.search_btn = gtk.Button('Search')
        self.search_btn.connect('clicked', self.do_search, 'search_btn')
                
    def create_treeview(self):
        self.liststore = gtk.ListStore(str)
        for i in range(5):
            self.liststore.append(["wotup"])
        self.treeview = gtk.TreeView(self.liststore)
        self.tcol = gtk.TreeViewColumn('Results')
        self.treeview.append_column(self.tcol)
        self.cell = gtk.CellRendererText()
        #self.cell.set_property('cell-background', 'cyan')
        self.tcol.pack_start(self.cell, True)
        self.tcol.add_attribute(self.cell, 'text', 0)
        
    def search_loop(self):
        in_str = ''
        while (in_str != 'exit'):
            in_str = raw_input('Enter search term\n')
            results = self.search_pairs(in_str)

    def update_liststore(self, data):
        self.liststore.clear()
        for item in data:
            #print item
            self.liststore.append([item[0]])
                    
    def do_search(self, widget, event, data=None):
        if (data == 'entry' and  event.keyval == 65293) or data == 'search_btn':
            search_string = self.entry.get_text()
            results = self.search_pairs(search_string)
            self.update_liststore(results)
        else:
            pass

    def search_pairs(self, word):
        matches = []
        for i in range(len(self.pairs)):
            found = re.search(word, self.pairs[i][1])
            
            if found:
                matches.append(self.pairs[i])

        return matches
                
        #print 'Found %d sentences containing "%s".'%(len(matches), word)


def main():
    gtk.main()

if __name__ == '__main__':
    if not sys.argv:
        print 'Provide location of corpus file.'
        sys.exit(1)
    else:
        Corpus(sys.argv[1])
        main()
