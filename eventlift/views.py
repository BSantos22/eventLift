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


@app.route('/profile')
def profile():
    if session.get('username'):
        if not session['username']:
            return redirect(url_for('index'))
    return render_template('profile.html')


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

@app.route('/create_event', methods=['POST', 'GET'])
def create_event():
    if request.method == 'POST':
        name = request.form['name']
        local = request.form['local']
        sdate = request.form['sdate']
        edate = request.form['edate']
        create_event = models.create_event(name, local, sdate, edate)

        if create_event:
            event = models.get_event(name, local)
            return redirect(url_for('event', rowid=event[0][4]))
        else:
            return "Failed to register"
    else:
        return render_template('create_event.html')

@app.route('/event/<eventid>/create_lift', methods=['POST', 'GET'])
def create_lift(eventid):
    if request.method == 'POST':
        ownerid = models.get_userid(session['username'])
        price = request.form['price']
        twoway = request.form['twoway']
        lftime = request.form['lftime']
        lfplace = request.form['lfplace']
        numseats = request.form['numseats']
        emptyseats = request.form['emptyseats']
        if emptyseats < numseats:
            create_lift = models.create_lift(ownerid, int(eventid), price, twoway, lftime, lfplace, numseats, emptyseats)
        else:
            create_lift = False;

        if create_lift:
            return redirect(url_for('event', rowid=eventid))
        else:
            return "Failed to register"
    else:
        return render_template('create_lift.html')
