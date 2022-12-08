from flask import *

import data

app = Flask(__name__)

@app.route("/")
def index():
    cities = data.get_cities()
    return render_template("index.html", len = len(cities), cities =cities )

@app.route("/city/<cityname>")
def city_universities(cityname):
    univs = data.get_universities(cityname.split(',')[0])

    return render_template("city.html", len=len(univs), univs=univs, city=cityname)

