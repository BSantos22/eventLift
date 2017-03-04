from eventlift import app, models
from flask import render_template, request, redirect, url_for, session


@app.route('/')
def index():
    return render_template('home.html')


@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        registered = models.get_users(username, password)
        if registered:
            session['username'] = username
            return redirect(url_for('index'))
        else:
            return "Show failed login page"
    else:
        return render_template('login.html')


@app.route('/register', methods=['POST', 'GET'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        registered = models.register_user(username, password, email)
        if registered:
            session['username'] = username
            return redirect(url_for('index'))
        else:
            return "Failed to register"
    else:
        return render_template('register.html')


@app.route('/signout')
def signout():
    session.clear()
    return redirect(url_for('index'))


@app.route('/event/<rowid>')
def event(rowid):
    event = models.get_event_by_id(rowid)
    lifts = models.get_lifts_from_event(event[0][0], event[0][1])
    return render_template('event.html', event=event, lifts=lifts)
