#!/usr/bin/python
import sys
import re

def parse_dict(edict):
    """Parses the edict file.
    
    Arguments:
    - `edict`: Edict file.
    """
    s = edict.read()
    #print re.findall('\([0-9]{1,2}\)', s)
    #print re.findall('\(P\)',s)
    lines = s.split('\n')
    for line in lines[24000:25000]:
        print len(line.split('(P)'))
                   

def main():
    """
    """
    f = ''
    try:
        dic = sys.argv[1]
        f = open(dic, 'r')
    except IndexError:
        print 'Pass edict file as parameter.'
        sys.exit(1)
    except IOError:
        print 'File does not exist or cannot be accessed.'
        sys.exit(1)
    
    parse_dict(f)

if __name__ == '__main__':
    main()
