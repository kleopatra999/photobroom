#!/usr/bin/python

import sqlite3
import re, os

def get_keepdir_idx(dirs):
    idx = -1
    print "================ Select a keepdir  ==============="
    while (idx < 0 or idx >= len(dirs)):
        i = 0
        for dir in dirs:
            print i, ":", dir
            i = i + 1

        choice = raw_input("Keepdir: ")
        try:
            idx = int(choice)
            if (idx < 0 or idx >= len(dirs)):
                raise RuntimeError("Invalid choice")
        except:
            print "Invalid choice. Try again."
            idx = -1

    return idx

def set_keepdir(cursor, path):
    sql = "UPDATE directories SET keep = 1 WHERE path = ?"
    cursor.execute(sql, (path,))


conn = sqlite3.connect("db")
conn.isolation_level = None

c = conn.cursor()
batfp = open("script.bat", "w")
batfp.write('md Temp\n')

shfp = open("script.sh", "w")
shfp.write('#!/bin/sh\n')
shfp.write('mkdir Temp\n')

for row in c.execute('SELECT sha FROM photos GROUP BY sha HAVING COUNT(sha) > 1'):
    sha = row[0]
    c2 = conn.cursor()

    files = []
    dirs = []
    keepidx = -1
    sql = 'SELECT filename,path,keep FROM photos as P join directories as D ON P.diridx = D.rowid WHERE sha=?'
    i = 0
    for subrow in c2.execute(sql, (sha,)):
        [filename,path,keep] = subrow
        files.append(os.path.join(path, filename))
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
    batfp.write("REM Original: " + kept + "\n")
    shfp.write("# Original: " + kept + "\n")
    for file in files:
        dotpos = file.rfind('.')
        if dotpos > 0:
            suffix = file[dotpos:]
        else:
            suffix = ""
        batfp.write('MOVE /Y "{0}" Temp\\{1}{2}\n'.format(file,sha, suffix))
        shfp.write('mv -f  "{0}" Temp/{1}{2}\n'.format(file,sha, suffix))
    batfp.write("\n")
    shfp.write("\n")


batfp.close()
shfp.close()

