import numpy as np

import datetime as dt

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask,jsonify

#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///../Resources/hawaii.sqlite")

Base = automap_base()
Base.prepare(autoload_with=engine)

Measurement = Base.classes.measurement
Station = Base.classes.station

session = Session(engine)

#################################################
# Flask Setup
#################################################
app = Flask(__name__)



#################################################
# Flask Routes
#################################################
@app.route("/")
def welcome():
    return (
        f"Welcome to the Climate Analysis API!<br/>"
        f"Available Routes:<br/>"
        f"api/v1.0/precipitation<br/>"
        f"api/v1.0/stations<br/>"
        f"api/v1.0/tobs<br/>"
        f"api/v1.0/<start><br/>"
        f"api/v1.0/<start>/<end>"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    year_ago = dt.date(2017, 8, 23) - dt.timedelta(days=365)

    results = session.query(Measurement.date, Measurement.prcp).\
        filter(Measurement.date >= year_ago).\
        order_by(Measurement.date).all()
    
    session.close()
    
    precipitation = list(np.ravel(results))

    return jsonify(precipitation)

@app.route("/api/v1.0/stations")
def stations():
    results = session.query(Station.station).all()

    session.close()

    stations = list(np.ravel(results))

    return jsonify(stations)

@app.route("/api/v1.0/tobs")
def tobs():
    year_ago = dt.date(2017, 8, 23) - dt.timedelta(days=365)

    results = session.query(Measurement.tobs).\
        filter(Measurement.station == 'USC00519281').\
        filter(Measurement.date >= year_ago).all()

    session.close()

    tobs = list(np.ravel(results))

    return jsonify(tobs)

@app.route("/api/v1.0/<start>")
def start(start):
    results = session.query(func.min(Measurement.tobs), func.max(Measurement.tobs), func.avg(Measurement.tobs)).\
        filter(Measurement.date >= start).all()

    session.close()

    temps = list(np.ravel(results))

    return jsonify(temps)

@app.route("/api/v1.0/<start>/<end>")
def start_end(start, end):
    results = session.query(func.min(Measurement.tobs), func.max(Measurement.tobs), func.avg(Measurement.tobs)).\
        filter(Measurement.date >= start).\
        filter(Measurement.date <= end).all()

    session.close()

    temps = list(np.ravel(results))

    return jsonify(temps)

if __name__ == '__main__':
    app.run(debug=True)