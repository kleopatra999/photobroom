#!/usr/bin/python

import sys,os,stat
import hashlib

def print_hash(file):
    m = hashlib.sha224()
    with open(file) as fp:
        buf = fp.read(4096)
        while len(buf) > 0:
            m.update(buf)
            buf = fp.read(4096)

    str = m.hexdigest()
    print str + " " + file

def walktree(dir):
    names = os.listdir(dir)

    for name in names:
        path = os.path.join(dir, name)
        mode = os.lstat(path).st_mode
        if stat.S_ISDIR(mode):
            walktree(path)
        elif stat.S_ISREG(mode):
            print_hash(path)
        

if len(sys.argv) != 2:
    raise RuntimeError("usage: inventroy.py topdir")

topdir = sys.argv[1]

walktree(topdir)
