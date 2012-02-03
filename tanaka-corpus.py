#!/usr/bin/python

import sys, re, pygtk
pygtk.require('2.0')
import gtk

class Corpus:
    
    
    
    def __init__(self, corpus_loc=None):
        
        self.read_corpus(corpus_loc)

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
        v3.pack_start(self.menubar, False, False, 0)
        v3.pack_start(scr_win, True, True, 0)
        v3.pack_start(v1, False, False,0)
        v3.pack_end(self.status, False, False, 0)

        self.window.add(v3)
        self.window.set_focus(self.entry)
        self.window.show_all()

    def make_gui_widgets(self):
        self.create_entry()
        self.create_buttons()
        self.create_treeview()
        self.create_statusbar()
        self.create_menubar()
        
    def create_entry(self):
        self.entry = gtk.Entry()
        self.entry.set_visibility(True)
        #self.entry.connect('key-press-event', self.do_search, 'entry')
        
    def create_statusbar(self):
        self.status = gtk.Statusbar()

        
    def create_menubar(self):
        self.menubar = gtk.MenuBar()
        filemenu = gtk.Menu()
        file_ = gtk.MenuItem("File")
        file_.set_submenu(filemenu)

        open_ = gtk.MenuItem("Open")
        open_.connect("activate", self.open_dialogue)
        filemenu.append(open_)
        
        exit_ = gtk.MenuItem("Exit")
        exit_.connect("activate", gtk.main_quit)
        filemenu.append(exit_)

        self.menubar.append(file_)

    def open_dialogue(self, widget):
        dia = gtk.FileChooserDialog(title='Corpus Location', action=gtk.FILE_CHOOSER_ACTION_OPEN, buttons=(gtk.STOCK_CANCEL,gtk.RESPONSE_CANCEL,gtk.STOCK_OPEN,gtk.RESPONSE_OK))
                
        res = dia.run()

        if res == gtk.RESPONSE_OK:
            self.read_corpus(dia.get_filename())
       
        dia.destroy()

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
                
    def create_buttons(self):
        self.search_btn = gtk.Button('Search')
        self.search_btn.connect('clicked', self.do_search, 'search_btn')
                
    def create_treeview(self):
        self.liststore = gtk.ListStore(str, str)
        self.treeview = gtk.TreeView(self.liststore)

        cell = gtk.CellRendererText()
        tcol = gtk.TreeViewColumn('Results', cell, markup=0)
        self.treeview.append_column(tcol)
        
        #tcol.pack_start(cell, True)
        tcol.add_attribute(cell, 'text', 0)
        self.treeview.set_tooltip_column(1)
        
    def search_loop(self):
        in_str = ''
        while (in_str != 'exit'):
            in_str = raw_input('Enter search term\n')
            results = self.search_pairs(in_str)

    def no_dict_dialog(self):
        label = gtk.Label('Cannot find any data. You have probably not yet input the location of the Tanaka Corpus.')
        label.set_line_wrap(True)
        label.set_justify(gtk.JUSTIFY_CENTER)
        label.show()
        dialog = gtk.Dialog('Cannot find dictionary', self.window, gtk.DIALOG_MODAL, buttons=(gtk.STOCK_OK, gtk.RESPONSE_OK))
        dialog.vbox.pack_start(label)
        dialog.run()       
        dialog.destroy()

    def update_liststore(self, data, search_word):
        self.liststore.clear()
        for item in data:
            sp = item[0].split('\t')
            jp = sp[0]
            en,id_ = sp[1].split('#ID=')
            self.liststore.append([self.apply_markup(jp, search_word), en])

    def apply_markup(self, sentence, word):
        self.highlight_colour = 'red'
        return sentence.replace(word, '<span foreground="red">%s</span>'%(word))
                    
    def do_search(self, widget, event, data=None):
        if not self.corpus_loc:
            self.no_dict_dialog()
        else:
            search_string = self.entry.get_text()
            results = self.search_pairs(search_string)
            self.update_liststore(results, search_string)
        
    def search_pairs(self, word):
        matches = []
        for i in range(len(self.pairs)):
            found = re.search(word, self.pairs[i][1])
            
            if found:
                matches.append(self.pairs[i])

        self.status.push(1, 'Found %d sentences containing "%s".'%(len(matches), word))

        return matches


def main():
    gtk.main()

if __name__ == '__main__':
    if len(sys.argv) == 1:
        Corpus()
    else:
        Corpus(sys.argv[1])
    main()
