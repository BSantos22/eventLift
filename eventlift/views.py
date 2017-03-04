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
