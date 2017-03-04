from flask import Flask

app = Flask(__name__)
app.secret_key = 'di47?Ws.316k4K!afY16xC3#Odh99L'

import eventlift.views
