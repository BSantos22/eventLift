from eventlift import app, models
from flask import render_template

@app.route('/')
def index():
    return render_template('home.html')

@app.route('/login')
def index():
    return render_template('login.html')
