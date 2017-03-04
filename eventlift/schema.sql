DROP TABLE IF EXISTS Users;
DROP TABLE IF EXISTS Events;
DROP TABLE IF EXISTS Lifts;
DROP TABLE IF EXISTS Reservations;

CREATE TABLE Users (
    user VARCHAR(32) NOT NULL,
    pass VARCHAR(32) NOT NULL,
    email VARCHAR(64) NOT NULL,
    reputation INTEGER,
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
    owner REFERENCES Users(rowID),
    event REFERENCES Events(rowID),
    price INTEGER NOT NULL,
    twoway BOOLEAN NOT NULL,
    lftime VARCHAR(32) NOT NULL,
    numseats INTEGER NOT NULL,
    emptyseats INTEGER NOT NULL CHECK(emptyseats > 0)
);

CREATE TABLE Reservations(
    event REFERENCES Events(rowID),
    user REFERENCES Events(rowID),
    numseats INTEGER NOT NULL CHECK (numseats > 0)
);


CREATE TRIGGER IF NOT EXISTS RemoveEmptySeat
    AFTER INSERT ON Reservations
    BEGIN
        UPDATE Lifts
        SET emptyseats = emptyseats - NEW.numseats
        WHERE (Lifts.rowID = Reservations.event);
    END;

CREATE TRIGGER IF NOT EXISTS CancelReservation
    AFTER DELETE ON Reservations
    BEGIN
        Update Lifts
        SET emptyseats = emptyseats - OLD.numseats
        WHERE (Lifts.rowID = Reservations.event);
    END;
