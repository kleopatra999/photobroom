
DROP TABLE photos;
DROP TABLE directories;

CREATE TABLE directories (
    path varchar UNIQUE,
    keep     BOOLEAN
);

CREATE TABLE photos (
    sha    CHAR(40) NOT NULL,
    diridx  int, -- rowid from directories
    filename VARCHAR(4096) NOT NULL
);

