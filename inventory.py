#!/usr/bin/python

import sys,os,stat
import hashlib
import sqlite3

def create_schema(dbconn):
    sql = """
DROP TABLE IF EXISTS photos;
DROP TABLE IF EXISTS directories;

CREATE TABLE directories (
    path varchar UNIQUE,
    keep     BOOLEAN
);

CREATE TABLE photos (
    sha    CHAR(40) NOT NULL,
    diridx  int, -- rowid from directories
    filename VARCHAR(4096) NOT NULL
);
    """
    cursor = dbconn.cursor()
    cursor.executescript(sql)

def add_to_db(cursor, sha, dir, file):
    sql = 'INSERT OR IGNORE INTO directories VALUES(?, ?)'
    cursor.execute(sql, (dir, 0))

    diridx_sql = 'SELECT directories.rowid FROM directories WHERE path = ?'
    sql = 'INSERT INTO photos VALUES(?, ({0}), ?)'.format(diridx_sql)
    cursor.execute(sql, (sha, dir, file))


def print_hash(cursor, dir, file):
    path = os.path.join(dir, file)
    m = hashlib.sha224()
    with open(path) as fp:
        buf = fp.read(4096)
        while len(buf) > 0:
            m.update(buf)
            buf = fp.read(4096)

    str = m.hexdigest()
    # print str + " " + path
    add_to_db(cursor, str, dir, file)

def walktree(cursor, dir):
    names = os.listdir(dir)

    for name in names:
        path = os.path.join(dir, name)
        mode = os.lstat(path).st_mode
        if stat.S_ISDIR(mode):
            walktree(cursor, path)
        elif stat.S_ISREG(mode):
            print_hash(cursor, dir, name)
        

if len(sys.argv) != 2:
    raise RuntimeError("usage: inventroy.py topdir")

topdir = sys.argv[1]

conn = sqlite3.connect("db")
cursor = conn.cursor()
create_schema(conn)
walktree(cursor, topdir)
conn.commit()
