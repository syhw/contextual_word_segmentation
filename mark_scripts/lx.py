"""lx.py -- Mark Johnson, 24th Febuary 2005

lx contains utility functions for the other programs
in this directory."""

import os, os.path

def incr(d, k, inc=1):
    """incr adds inc to the value of d[k] if d[k] is defined,
    or sets d[k] to inc if d[k] is undefined.

    d is the dictionary being incremented.
    k is the dictionary key whose value is incremented.
    inc is the size of the increment (default 1)."""
    if k in d:
        d[k] += inc
    else:
        d[k] = inc

# Sorting

def sort(xs):
    """Returns a list containing the same elements as xs, but in sorted order."""
    xs.sort()
    return xs

def cmp2nd(x, y):
    """Comparson function of 2nd items in x and y.

    To sort a list in order on the 2nd item in each tuple, use
    lst.sort(lx.cmp2nd) """
    return cmp(x[1], y[1])

def sort2nd(xs):
    """Returns a list containing the same elements as xs, but sorted by their
    second elements."""
    xs.sort(cmp2nd)
    return xs

def icmp2nd(x, y):
    """Inverse comparson function of 2nd items in x and y.

    To sort a list in inverse order on the 2nd item in each tuple, use
    lst.sort(lxutil.icmp2nd) """   
    return -cmp(x[1], y[1])

def isort2nd(xs):
    """Returns a list containing the same elements as xs, but sorted by their
    second elements in reverse."""
    xs.sort(icmp2nd)
    return xs

# Finding all files that meet a condition

def findfiles(topdir, file_re):
    """Returns a list of filenames below dir whose names match filenameregex."""
    filenames = []
    for root, dirs, files in os.walk(topdir):
        for file in files:
            if file_re.match(file):
                filenames.append(os.path.join(root, file))
    return filenames
