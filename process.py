#!/usr/bin/python
import sqlite3

def get_keepdir_idx(dirs):
    for dir in dirs:
        print dir
    choice = raw_input("Which one is original: ")
    idx = int(choice)
    # Validate input (FIXME)
    return idx

def set_keepdir(cursor, path):
    sql = "UPDATE directories SET keep = 1 WHERE path = ?"
    cursor.execute(sql, (path,))


conn = sqlite3.connect("db")
conn.isolation_level = None

c = conn.cursor()
fp = open("script.sh", "w")

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
    fp.write("# Original:"+ kept + "\n")
    for file in files:
        fp.write("DEL " + file + "\n")
    fp.write("\n")


fp.close()
  
