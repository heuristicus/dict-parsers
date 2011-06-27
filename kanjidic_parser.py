#!/usr/bin/python
import sys
import re

def read_dict(dict_file):
    """Reads the kanjidic file.
    """
    s = dict_file.read()
    # Kanji defs are line spaced, so split on these line breaks.
    line_split = s.split('\n')
    # List in which to store the stuff we want to keep.
    parsed = []
    # Last index contains nothing, so ignore it.
    for line in line_split[1:-1]:
        # Bits on each line are space separated, so split
        # these. Problematic. Meanings with more than one word also
        # get split - do not want that. e.g. {beautiful (as a jewel)}
        # -> ['{beautiful', '(as', 'a', 'jewel)}']. Split on '{'
        # instead, and then process the initial segment instead of the
        # whole string? Saves having to find the index of the meanings
        # as well, will be space_split[1:] if this split is done
        # first.

        space_split = line.split(' ')
        #for c in line.decode('utf-8'):
        #    print c
        #First index of the split list is the kanji.
        kanji = space_split[0]
        indices = get_indices(space_split)
        #print indices
        readings = space_split[indices[0]:indices[1]]
        classes = []
        for i in range(len(indices[1:-1])):
            prop_i = i+1
            # Append elements contained in the kanji definition from
            # the start of the current class to the start of the next
            # class, ignoring the class definition (e.g. T1).
            classes.append(space_split[indices[prop_i] + 1:indices[prop_i + 1]])
        # -1 to strip out the last index which is empty
        meanings = space_split[indices[-1]:-1]
        #print meanings
        #print kanji
        

def get_indices(str_):
    """Returns a tuple containing the positions in the string of:
        - The first kana
        - Any class markers (T1 for names, T2 for radicals)
        - The first english definition
    Arguments:
    - `str_`: String containing the kanji definition.
    """


def get_indices(list_):
    """Same as the above method, buts scans the string split on spaces
    instead of the raw string.
    
    Arguments:
    - `list_`: Kanji definition string split on spaces.
    """
    
    kana_found = False
    ind_list = []
    # really crude way of referencing index. Find a way to iterate over index and item in list.
    ind = 1
    # First index contains kanji, last index is blank enumerate the
    # list and then iterate over the items in it, with reference ind
    # referring to the item index.
    for ind, item in enumerate(list_[1:-1]):
        if not kana_found:
            # The ordinal range for kana characters in unicode is 12352-12543
            if 12352 <= ord(item.decode('utf-8')[0]) <= 12543:
                #print 'kana'
                ind_list.append(ind + 1)
                kana_found = True
        # Find classes in the line - denoted by T1/T2. Only take into
        # account those items which are at the start of a line (^)
        if re.search('^T[0-9]', item):
            ind_list.append(ind + 1)
            #print 'special'
            print item
        if item[0] == '{':
            ind_list.append(ind + 1)
            #print 'meaning'
            # found the last index we need, so stop the loop
            break
        ind += 1

    return ind_list

def main():
    """Attempts to parse the kanjidic file passed as an argument to the script.
    """
    f = ''
    try:
        # Store dict loc by changing a string in here?  e.g default
        # file has no dictionary location - when one is entered, a
        # string which contains the file location is edited by writing
        # to this file. The script checks if this is different from
        # the default string, and if so attempts to read that file
        # location. If it doesn't exist, ask for actual location and
        # update or complain. Maybe kind of annoying.
        dict_loc = sys.argv[1]
        f = open(dict_loc, 'r')
    except IndexError:
        print 'Pass kanjidic location as a parameter.'
    except IOError:
        print 'File does not exist or cannot be accessed.'
    
    read_dict(f)

if __name__ == '__main__':
    main()
