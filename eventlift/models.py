from eventlift import app
import sqlite3

DATABASE = 'eventlift/schema.db'


def register_user(username, password, email, phone):
    users = exists_user(username)
    if not users:
        db = sqlite3.connect(DATABASE)
        cur = db.cursor()
        cur.execute('INSERT INTO Users (user,pass,email, phone) VALUES (?,?,?,?)',
                    (username, password, email, phone))
        db.commit()
        db.close()
        return True
    else:
        return False


def exists_user(username):
    db = sqlite3.connect(DATABASE)
    cur = db.cursor()
    cur.execute('SELECT user FROM Users WHERE user=?', (username,))
    users = cur.fetchall()
    db.close()
    if not users:
        return False
    return True


def get_users(username, password):
    db = sqlite3.connect(DATABASE)
    cur = db.cursor()
    cur.execute('SELECT user,pass FROM Users WHERE user=? AND pass=?', (username, password))
    users = cur.fetchall()
    db.close()
    return users


def get_event(name, local):
    db = sqlite3.connect(DATABASE)
    cur = db.cursor()
    cur.execute('SELECT *,rowid FROM Events WHERE name=? AND local=?', (name, local))
    event = cur.fetchall()
    db.close()
    return event

def get_event_by_id(rowid):
    db = sqlite3.connect(DATABASE)
    cur = db.cursor()
    cur.execute('SELECT *,rowid FROM Events WHERE rowid=?', rowid)
    event = cur.fetchall()
    db.close()
    return event

def get_lifts_from_event(name, local):
    event = get_event(name, local)
    db = sqlite3.connect(DATABASE)
    cur = db.cursor()
    cur.execute('SELECT * FROM Lifts WHERE event=?', (event[0][4],))
    lifts = cur.fetchall()
    db.close()
    return lifts


def create_event(name, local, stdate, endate):
    event = get_event(name, local)
    if not event:
        db = sqlite3.connect(DATABASE)
        cur = db.cursor()
        cur.execute('INSERT INTO Events (name, local, stdate, endate) VALUES (?,?,?,?)',
                    (name, local, stdate, endate))
        db.commit()
        db.close()
        return True
    else:
        return False

def create_lift(owner, event, price, twoway, lftime, lfplace, numseats, emptyseats):
    db = sqlite3.connect(DATABASE)
    cur = db.cursor()
    cur.execute('INSERT INTO Lifts (owner, event, price, twoway, lftime, lfplace, numseats, emptyseats) values (?,?,?,?,?,?,?,?)', (owner, event, price, twoway, lftime, lfplace, numseats, emptyseats))
    db.commit()
    db.close()
    return True

def create_reservation(name, local, numseats):
    username = session['username']
    userid = get_userid(username)
    event = get_event(name, local)

    if event:
        db = sqlite3.connect(DATABASE)
        cur = db.cursor()
        cur.execute('INSERT INTO Reservations(event, user, numseats) VALUES (?,?,?)',
                    (event['rowid'], userid, numseats))
        db.commit()
        db.close()
        return True
    else:
        return False


def get_userid(username):
    db = sqlite3.connect(DATABASE)
    cur = db.cursor()
    cur.execute('SELECT rowid FROM Users WHERE user=?', (username,))
    userid = cur.fetchall()
    db.close()
    return userid


def get_user_data(username):
    db = sqlite3.connect(DATABASE)
    cur = db.cursor()
    cur.execute('SELECT user, email, phone FROM Users WHERE user=?', (username,))
    userdata = cur.fetchall()
    db.close()
    return userdata

def get_username_by_id(rowid):
    db = sqlite3.connect(DATABASE)
    cur = db.cursor()
    cur.execute('SELECT user FROM Users WHERE rowid=?', (rowid,))
    name = cur.fetchall()
    db.close()
    return name

def get_user_lifts(username):
    db = sqlite3.connect(DATABASE)
    cur = db.cursor()
    userid = get_userid(username)[0][0]
    cur.execute('SELECT * FROM Lifts JOIN Events ON (Lifts.event = Events.rowid) WHERE owner=?', (userid,))
    user_lifts = cur.fetchall()
    db.close()
    return user_lifts

def get_user_reservations(username):
    db = sqlite3.connect(DATABASE)
    cur = db.cursor()
    userid = get_userid(username)[0][0]
    cur.execute('SELECT * FROM Reservations JOIN Lifts ON Lifts.rowid = Reservations.lift JOIN Events ON  Lifts.event = Events.rowid WHERE Reservations.user=?', (userid,))
    user_reservations = cur.fetchall()
    db.close()
    return user_reservations

def search_lifts(search):
    db = sqlite3.connect(DATABASE)
    cur = db.cursor()
    string = "%" + str(search) + "%"
    cur.execute('SELECT *,l.rowid FROM Lifts l LEFT JOIN Events e ON l.event = e.rowid WHERE event LIKE ? OR lfplace LIKE ?', (string, string))
    results = cur.fetchall()
    db.close()
    return results

def search_events(search):
    db = sqlite3.connect(DATABASE)
    cur = db.cursor()
    string = "%" + str(search) + "%"
    cur.execute('SELECT *,rowid FROM Events WHERE local LIKE ? OR name LIKE ?', (string, string))
    results = cur.fetchall()
    db.close()
    return results

def get_lift_by_id(rowid):
    db = sqlite3.connect(DATABASE)
    cur = db.cursor()
    cur.execute('SELECT * FROM Lifts JOIN Events ON Lifts.event = Events.rowID WHERE Lifts.rowid=?', (rowid))
    lift = cur.fetchall()
    db.close()
    return lift;
