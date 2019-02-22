import re
import sys
import operator
from collections import defaultdict


def tokenize(s, rmdr, freq):
    """Checks for alphanumeric characters in file block. If found, save index
    until end of token is found. Then, normalize and save token in frequency
    dictionary and repeat until file is completely tokenized. If current token
    continues to next file block, save it as remainder"""
    i = 0
    start = 0
    for char in s:
        if re.match("[a-zA-Z0-9]", char) == None:
            if i - start + len(rmdr) > 0:
                freq[rmdr + s[start:i].lower()] += 1
                rmdr = ""
            start = i+1
        i += 1
    if i - start > 0:
        return rmdr + s[start:i].lower()
    else:
        return ""

def print_freq(freq):
    """ Prints a sorted version of the frequency dictionary"""
    sorted_freq = sorted(freq.items(), key=operator.itemgetter(0))
    sorted_freq = sorted(sorted_freq, key=operator.itemgetter(1), reverse=True)
    for token,n in sorted_freq:
        print("{}\t{}".format(token, n))
    return 0

def get_freq(file):
    """Reads file (10 KB at a time)into string and tokenizes the string"""
    freq = defaultdict(lambda: 0)
    s = file.read(10240)
    rmdr = ""
    while (len(s) > 0):
        rmdr = tokenize(s, rmdr, freq)
        s = file.read(10240)
    if (len(rmdr) > 0):
        freq[rmdr] += 1
    return freq

if __name__ == '__main__':
    """Opens file, constructs frequency dictionary, then prints it"""
    if len(sys.argv) == 2:
        file = open(sys.argv[1], "r", encoding="utf-8", errors="ignore")
        freq = get_freq(file)
        print_freq(freq)
