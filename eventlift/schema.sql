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
    twoway INTEGER NOT NULL,
    lftime VARCHAR(32) NOT NULL,
    lfplace VARCHAR(32) NOT NULL,
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
        WHERE (Lifts.rowID = NEW.event);
    END;

CREATE TRIGGER IF NOT EXISTS CancelReservation
    AFTER DELETE ON Reservations
    BEGIN
        Update Lifts
        SET emptyseats = emptyseats + OLD.numseats
        WHERE (Lifts.rowID = OLD.event);
    END;



INSERT INTO Users(user, pass, email, reputation) VALUES("U1", "P1", "asda@asdas.x", 0);
INSERT INTO Users(user, pass, email, reputation) VALUES("U2", "P2", "asda@asadas.x", 0);

INSERT INTO Events(name, local, stdate, endate) VALUES("PMR PO CRL", "Estádio José Alvalade", "04-03-2017 09:00", "04-03-2017 19:00");
INSERT INTO Events(name, local, stdate, endate) VALUES("BENFICA É MERDA", "TODO O LADO", "Algures em 1904 (dizem eles)", "PARA SEMPRE");

INSERT INTO Lifts(owner, event, price, twoway, lftime, lfplace, numseats, emptyseats) VALUES(1, 1, 0, 1, "08:55", "PRIMA DO PMR", 100, 100);

SELECT emptyseats FROM Lifts;

INSERT INTO Reservations(event, user, numseats) VALUES(1, 1, 20);

SELECT emptyseats FROM Lifts;

DELETE FROM Reservations WHERE rowID=1;

SELECT emptyseats FROM Lifts;
