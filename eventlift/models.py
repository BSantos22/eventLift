from eventlift import app
import sqlite3

DATABASE = 'eventlift/schema.db'


def register_user(username, password, email):
    users = exists_user(username)
    if not users:
        db = sqlite3.connect(DATABASE)
        cur = db.cursor()
        cur.execute('INSERT INTO Users (user,pass,email) VALUES (?,?,?)',
                    (username, password, email))
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

def get_event(rowid):
    db = sqlite3.connect(DATABASE)
    cur = db.cursor()
    cur.execute('SELECT * FROM Events WHERE rowid=?', rowid)
    event = cur.fetchall()
    db.close()
    return event


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
    cur.execute('SELECT rowid FROM Users WHERE user=?', username)
    userid = cur.fetchall()
    db.close()
    return userid
