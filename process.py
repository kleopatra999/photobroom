#!/usr/bin/python

import sqlite3
import re

def get_keepdir_idx(dirs):
    idx = -1
    print "=============================================================="
    while (idx < 0 or idx >= len(dirs)):
        i = 0
        for dir in dirs:
            print i, ":", dir
            i = i + 1

        choice = raw_input("Keepdir: ")
        idx = int(choice)
    return idx

def set_keepdir(cursor, path):
    sql = "UPDATE directories SET keep = 1 WHERE path = ?"
    cursor.execute(sql, (path,))


conn = sqlite3.connect("db")
conn.isolation_level = None

c = conn.cursor()
fp = open("script.bat", "w")

for row in c.execute('SELECT sha FROM photos GROUP BY sha'):
    sha = row[0]
    c2 = conn.cursor()
    
    files = []
    dirs = []
    keepidx = -1
    sql = 'SELECT filename,path,keep FROM photos as P join directories as D ON P.diridx = D.rowid WHERE sha=?'
    i = 0
    for subrow in c2.execute(sql, (sha,)):
        [filename,path,keep] = subrow
        files.append(path + "/" + filename)
        dirs.append(path)
        if keep == 1:
            keepidx = i
        i = i + 1
    
    if keepidx == -1:
        keepidx = get_keepdir_idx(files)
        set_keepdir(c2, dirs[keepidx])

    kept =  files[keepidx]
    del files[keepidx]
    del dirs[keepidx]
    fp.write("REM Original:" + kept + "\n")
    for file in files:
        # MOVE "/mnt/Windows/Users/Sandeep/My Documents/My Pictures/2009/Jun/IMG_1058.JPG" Temp\000da5ab30312af3176e38cc03b292e43c524495
        file = re.sub('/mnt/Windows/Users/Sandeep/', '', file)
        file = re.sub('/', '\\\\', file)
        dotpos = file.rfind('.')
        if dotpos > 0:
            suffix = file[dotpos+1:]
        else:
            suffix = ""
        fp.write('MOVE "{0}" Temp\\{1}.{2}\n'.format(file,sha, suffix))
    fp.write("\n")


fp.close()
  
