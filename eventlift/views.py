from eventlift import app, models
from flask import render_template, request, redirect, url_for, session


@app.route('/')
def index():
    return render_template('home.html')


@app.route('/login', methods=['POST', 'GET'])
def login():
    if session.get('username'):
        if session['username']:
            return redirect(url_for('index'))
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
    if session.get('username'):
        if session['username']:
            return redirect(url_for('index'))
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        phone = request.form['phone']
        registered = models.register_user(username, password, email, phone)
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
    l = []
    for lift in lifts:
        ll = list(lift)
        l.append(ll)

    for lift in l:
        lift[0] = (models.get_username_by_id(lift[0]))[0][0]
        if lift[3] == 1:
            lift[3] = "Yes"
        else:
            lift[3] = "No"
    return render_template('event.html', event=event, lifts=l)
