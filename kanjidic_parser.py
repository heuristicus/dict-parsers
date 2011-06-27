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
        # Split on the {. Separates out the english meanings from the rest of the data
        meaning_split =  line.split('{')
        # First index of meaning_split contains everything but the
        # meanings, space separated.
        space_split = meaning_split[0].split(' ')
        #First index of the split list is the kanji.
        kanji = space_split[0]
        # Get indices for separation points in the string. First index
        # is the first occurrence of a kana in the list, the following
        # indicate classes, if they exist. T1 is kana used for names,
        # T2 for radical names.
        indices = get_indices(space_split)
        #print indices
        # The part of the list which contains readings is different
        # depending on whether there are classes present or not.
        classes = []
        if len(indices) == 1:
            readings = space_split[indices[0]:-1]
            #print readings
        else:
            readings = space_split[indices[0]:indices[1]]
            print indices
            # Loop over all indices containing references to classes
            for i in map(lambda x: x + 1, range(len(indices[1:]))):
                print len(indices[1:])
                sec_ind = -1 if len(indices[1:]) == 1 else indices[i + 1]
                #print space_split[indices[i] + 1: sec_ind]
        # -1 to strip out the last index which is empty
        meanings = meaning_split[1:]
        # Strip '} ' on the end of each meaning.
        for i, string in enumerate(meanings):
            meanings[i] = string[:-2]
        #meanings = space_split[indices[-1]:-1]
        

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
    # First index contains kanji, last index is blank. Enumerate the
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
        elif re.search('^T[0-9]', item):
            ind_list.append(ind + 1)
            #print 'special'
            #print item
        elif item[0] == '{':
            ind_list.append(ind + 1)
            #print 'meaning'
            # found the last index we need, so stop the loop
            break

    #for ind in ind_list:
    #    print list_[ind]
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
