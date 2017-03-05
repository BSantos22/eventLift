from eventlift import app, models
from flask import render_template, request, redirect, url_for, session


@app.route('/')
def index():
    return render_template('home.html')


@app.route('/search', methods=['GET'])
def search():
    search = request.args.get('search')
    searchtype = request.args.get('searchtype')
    if searchtype == "lift":
        lifts = models.search_lifts(search)
        results = []
        for lift in lifts:
            ll = list(lift)
            results.append(ll)

        for lift in results:
            lift[0] = (models.get_username_by_id(lift[0]))[0][0]
            if lift[3] == 1:
                lift[3] = "Yes"
            else:
                lift[3] = "No"
    elif searchtype == "event":
        results = models.search_events(search)
    else:
        return render_template('home.html')

    return render_template('search.html', results=results)


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
            return render_template('login.html', state="wrong")
    else:
        return render_template('login.html', state="clean")


@app.route('/register', methods=['POST', 'GET'])
def register():
    if session.get('username'):
        if session['username']:
            return redirect(url_for('index'))
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        password2 = request.form['password2']
        if password != password2:
            return render_template('register.html', state="wrong")
        email = request.form['email']
        phone = request.form['phone']
        registered = models.register_user(username, password, email, phone)
        if registered:
            session['username'] = username
            return redirect(url_for('index'))
        else:
            return render_template('register.html', state="duplicate")
    else:
        return render_template('register.html', state="clean")


@app.route('/profile')
def profile():
    if not session.get('username'):
        return redirect(url_for('index'))
    user_data = models.get_user_data(session['username'])
    user_lifts = models.get_user_lifts(session['username'])
    user_reservations = models.get_user_reservations(session['username'])
    return render_template('profile.html', user_data=user_data, user_lifts=user_lifts, user_reservations=user_reservations)


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
        ownerid = models.get_userid(session['username'])[0][0]
        price = request.form['price']
        twoway = request.form['twoway']
        lftime = request.form['lftime']
        lfplace = request.form['lfplace']
        numseats = request.form['numseats']
        emptyseats = numseats
        if emptyseats <= numseats:
            create_lift = models.create_lift(ownerid, int(
                eventid), price, twoway, lftime, lfplace, numseats, emptyseats)
        else:
            create_lift = False

        if create_lift:
            return redirect(url_for('event', rowid=eventid))
        else:
            return "Failed to register"
    else:
        return render_template('create_lift.html')


@app.route('/lift/<liftid>')
def view_lift(liftid):
    lift = models.get_lift_by_id(liftid)
    return render_template('lift.html', lift=lift, liftid=liftid)


@app.route('/join_lift', methods=['POST'])
def join_lift():
    liftid = request.form['lift']
    numseats = request.form['seats']
    models.create_reservation(session['username'], liftid, numseats)
    return redirect(url_for('view_lift', liftid=liftid))
