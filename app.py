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