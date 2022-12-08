from flask import *

import data

app = Flask(__name__)

@app.route("/")
def index():
    cities = data.get_cities()
    return render_template("index.html", len = len(cities), cities =cities )


