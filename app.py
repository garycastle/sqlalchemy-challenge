from flask import Flask, json, jsonify
import datetime as dt

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from sqlalchemy import inspect

engine = create_engine("sqlite:///./Resources/hawaii.sqlite", connect_args={'check_same_thread': False})

Base = automap_base()

Base.prepare(engine, reflect=True)

meas = Base.classes.measurement
station = Base.classes.station
session = Session(engine)

app = Flask(__name__)

@app.route("/")
def home():
	print("Homepage")
	return(f"Climate API!<br/>"
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/2016-01-01/<br/>"
        f"/api/v1.0/2016-01-01/2016-12-31/")

@app.route('/api/v1.0/precipitation/')
def precipitation():

    last_date = session.query(meas.date).order_by(meas.date.desc()).first().date
    last_year = dt.datetime.strptime(last_date, '%Y-%m-%d') - dt.timedelta(days=365)

    rain_results = session.query(meas.date, meas.prcp).\
    filter(meas.date >= last_year).\
    order_by(meas.date).all()

    p_dict = dict(rain_results)
    print(f"Results for Precipitation - {p_dict}")
    print("Out of Precipitation section.")
    return jsonify(p_dict) 


if __name__ == "__main__":
    app.run(debug=True)