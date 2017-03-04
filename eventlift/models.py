from eventlift import app
import sqlite3

DATABASE = 'eventlift/schema.db'

def register_user(username, password, email):
    users = get_users(username, password)
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


def get_users(username, password):
    db = sqlite3.connect(DATABASE)
    cur = db.cursor()
    cur.execute('SELECT user,pass FROM Users WHERE user=? AND pass=?', (username, password))
    users = cur.fetchall()
    db.close()
    return users
