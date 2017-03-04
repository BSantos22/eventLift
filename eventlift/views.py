from eventlift import app


@app.route('/')
def index():
    return "EventLift"
