#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import subprocess

PASS = "PASS"
FAIL = "FAIL"
UNRESOLVED = "UNRESOLVED"
count = 0

def testxml(parsefile):
    inputfile = open(parsefile,"r")
    c = inputfile.read()
    test(c)
    inputfile.close()

def write_xml(c):
    xml = open("input.xml","w")
    s = ""
    for (index,char) in c :
        s += char
    xml.write(s)
    xml.close()
    return s


def test(c):
    content = write_xml(c)
    global count
    count = count + 1
    print "Testing %d : %s" %(count,content),
    try :
        statu = subprocess.call(["python","xpcmd.py","input.xml"],shell=False,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
        if statu:
            print FAIL
            return FAIL
        else :
            print PASS
            return PASS
    except SyntaxError :
        return UNRESOLVED

def split(circumstances, n):
    """Split a configuration CIRCUMSTANCES into N subsets;
       return the list of subsets"""

    subsets = []
    start = 0
    for i in range(0, n):
        len_subset = int((len(circumstances) - start) / float(n - i) + 0.5)
        subset = circumstances[start:start + len_subset]
        subsets.append(subset)
        start = start + len(subset)

    assert len(subsets) == n
    for s in subsets:
        assert len(s) > 0

    return subsets

def listminus(c1,c2):
    s2 = {}
    for delta in c2:
        s2[delta] = 1

    c = []
    for delta in c1:
        if not s2.has_key(delta):
            c.append(delta)
    
    return c

def ddmin(circumstances, test):
    """Return a sublist of CIRCUMSTANCES that is a relevant configuration
       with respect to TEST."""
    
    assert test([]) == PASS
    assert test(circumstances) == FAIL

    n = 2
    while len(circumstances) >= 2:
        subsets = split(circumstances, n)
        assert len(subsets) == n

        some_complement_is_failing = 0
        for subset in subsets:
            complement = listminus(circumstances, subset)

            if test(complement) == FAIL:
                circumstances = complement
                n = max(n - 1, 2)
                some_complement_is_failing = 1
                break

        if not some_complement_is_failing:
            if n == len(circumstances):
                break
            n = min(n * 2, len(circumstances))

    return circumstances


def string_to_list(s):
        c = []
        for i in range(len(s)):
                c.append((i, s[i]))
        return c


if __name__ == '__main__':
    tests = {}
    circumstances = []

    # testxml(sys.argv[1])
    inputfile = open(sys.argv[1],"r")
    c = inputfile.read()
    circumstances = string_to_list(c)
    print "Circumstances :",
    circumstances = ddmin(circumstances,test)
    print circumstances
    fault = ""
    for (index,char) in circumstances :
        fault += char
    print "The failure-inducing input :'" +fault + "'"
    print "The count of testings : %d" %count
