DROP TABLE IF EXISTS Users;
DROP TABLE IF EXISTS Events;
DROP TABLE IF EXISTS Lifts;
DROP TABLE IF EXISTS Reservations;

CREATE TABLE Users (
    user VARCHAR(32) NOT NULL,
    pass VARCHAR(32) NOT NULL,
    email VARCHAR(64) NOT NULL,
    phone VARCHAR(16) NOT NULL,
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
    emptyseats INTEGER NOT NULL CHECK(emptyseats >= 0)
);

CREATE TABLE Reservations(
    lift REFERENCES Lifts(rowID),
    user REFERENCES Users(rowID),
    numseats INTEGER NOT NULL CHECK (numseats > 0)
);


CREATE TRIGGER IF NOT EXISTS RemoveEmptySeat
    AFTER INSERT ON Reservations
    BEGIN
        UPDATE Lifts
        SET emptyseats = emptyseats - NEW.numseats
        WHERE (Lifts.rowID = NEW.lift);
    END;

CREATE TRIGGER IF NOT EXISTS CancelReservation
    AFTER DELETE ON Reservations
    BEGIN
        Update Lifts
        SET emptyseats = emptyseats + OLD.numseats
        WHERE (Lifts.rowID = OLD.lift);
    END;



INSERT INTO Users(user, pass, email, phone, reputation) VALUES("U1", "P1", "asda@asdas.x", 95656589864, 0);
INSERT INTO Users(user, pass, email, phone, reputation) VALUES("U2", "P2", "asda@asadas.x", 6512132656, 0);

INSERT INTO Events(name, local, stdate, endate) VALUES("Event 1", "UPC", "04-03-2017 09:00", "04-03-2017 19:00");
INSERT INTO Events(name, local, stdate, endate) VALUES("Event 2", "Airport", "05/03/2017 08:00", "05/03/2017 10:00");

INSERT INTO Lifts (owner, event, price, twoway, lftime, lfplace, numseats, emptyseats) values (2, 2, 9, 1, '12/23/2016', 'Indonesia', 1, 1);
INSERT INTO Lifts (owner, event, price, twoway, lftime, lfplace, numseats, emptyseats) values (2, 1, 47, 1, '6/21/2016', 'Philippines', 7, 1);
INSERT INTO Lifts (owner, event, price, twoway, lftime, lfplace, numseats, emptyseats) values (2, 2, 35, 0, '4/12/2016', 'China', 8, 1);
INSERT INTO Lifts (owner, event, price, twoway, lftime, lfplace, numseats, emptyseats) values (1, 2, 21, 0, '12/14/2016', 'Poland', 6, 2);
