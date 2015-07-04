#!/usr/bin/python

import fileinput;
import re

print "BEGIN;"
print "DELETE FROM photos;"
for line in fileinput.input():
    line = line[:-1]
    #260ed67aad25a6485ff1b0ac3dc0b23160648ca9  /mnt/Windows/Users/Sandeep/My Documents/My Pictures/Downloaded Albums/101841430187657132905/Cards/.picasa.ini
    sha = line[:40]
    rest = line[42:]
    idx = rest.rfind('/')
    if idx == -1:
        raise RuntimeError("Invalid line: " + line)
    filename = rest[idx+1:]
    path = rest[:idx]
    print "INSERT OR IGNORE INTO directories VALUES('{0}', 0);".format(path)
    diridx_sql = "SELECT directories.rowid FROM directories WHERE path = '{0}'".format(path)
    print "INSERT INTO photos VALUES('{0}', ({1}), '{2}');".format(sha, diridx_sql, filename)
print "COMMIT;"
