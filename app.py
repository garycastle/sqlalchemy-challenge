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
	return(f"Climate API<br/>"
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

@app.route('/api/v1.0/stations/')
def stations():
    
    station_list = session.query(station.station)\
    .order_by(station.station).all() 
    print()
    print("Station List:")   
    for row in station_list:
        print (row[0])

    return jsonify(station_list)

@app.route('/api/v1.0/tobs/')
def tobs():
    
    last_date = session.query(meas.date).order_by(meas.date.desc()).first().date
    last_year = dt.datetime.strptime(last_date, '%Y-%m-%d') - dt.timedelta(days=365)

    temp_obs = session.query(meas.date, meas.tobs)\
        .filter(meas.date >= last_year)\
        .order_by(meas.date).all()
    print()
    print(temp_obs)
    return jsonify(temp_obs)


# @app.route('/api/v1.0/2016-01-01/')

# def calc_temps_start(start_date):
# start_date = '2016-01-01'
#     print(start_date)
    
#     select = [func.min(meas.tobs), func.avg(meas.tobs), func.max(meas.tobs)]
#     result_temp = session.query(*select).\
#         filter(meas.date >= start_date).all()
#     print()
#     print(f"Calculated temp for start date {start_date}")
#     print(result_temp)
#     return jsonify(result_temp)

# @app.route('/api/v1.0/2016-01-01/2016-12-31/')
# start_date = '2016-01-01'
# end_date = '2016-12-31'
# def calc_temps_start_end(start_date, end_date):

    
#     select = [func.min(meas.tobs), func.avg(meas.tobs), func.max(meas.tobs)]
#     result_temp = session.query(*select).\
#         filter(meas.date >= start_date).filter(meas.date <= end_date).all()
#     print()
#     print(f"Calculated temp for start date {start_date} & end date {end_date}")
#     print(result_temp)

#     return jsonify(result_temp)



if __name__ == "__main__":
    app.run(debug=True)