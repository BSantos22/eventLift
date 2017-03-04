from eventlift import app, models


@app.route('/')
def index():
    return 'EventLift'
