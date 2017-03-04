DROP TABLE IF EXISTS Users;
DROP TABLE IF EXISTS Events;
DROP TABLE IF EXISTS Lifts;

CREATE TABLE Users (
    user VARCHAR(32) NOT NULL,
    pass VARCHAR(32) NOT NULL,
    email VARCHAR(64) NOT NULL,
    UNIQUE(user),
    UNIQUE(email)
);

CREATE TABLE Events(
    name VARCHAR(64) NOT NULL,
    local VARCHAR(32) NOT NULL,
    stdate VARCHAR(32) NOT NULL,
    endate VARCHAR(32) NOT NULL,
    PRIMARY KEY(name, local)
);

CREATE TABLE Lifts(
    event REFERENCES Events(rowID),
    price INTEGER NOT NULL,
    twoway BOOLEAN NOT NULL,
    lftime VARCHAR(32) NOT NULL,
    numplaces INTEGER NOT NULL,
    emptyplaces INTEGER NOT NULL
);
