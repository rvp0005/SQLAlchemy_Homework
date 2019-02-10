import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify


#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create our session (link) from Python to the DB
session = Session(engine)

#################################################
# Flask Setup
#################################################
app = Flask(__name__)

@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start><br/>"
        f"/api/v1.0/<start>/<end><br/>"
    )


@app.route("/api/v1.0/precipitation")
def precipitation():
    rain_results = session.query(Measurement.date, Measurement.prcp).all()

    precipitation_data = []

    for data in rain_results:
        prec_dict= {}
        prec_dict["Date"]= data.date
        prec_dict["Precip"]= data.prcp
        precipitation_data.append(prec_dict)

    return jsonify(precipitation_data)


@app.route("/api/v1.0/stations")
def stations():
    station_results = session.query(Station.station, Station.name).all()

    station_data = []

    for data in station_results:
        station_dict= {}
        station_dict["Station_ID"]= data.station
        station_dict["Name"]= data.name
        station_data.append(station_dict)

    return jsonify(station_data)

@app.route("/api/v1.0/tobs")
def tobs():
    query_date = "2016-08-23"
    temp_results= session.query(Measurement.date, Measurement.tobs).\
                    filter(Measurement.date > query_date).all()

    temp_data = []

    for data in temp_results:
        temp_dict= {}
        temp_dict["Date"]= data.date
        temp_dict["Tobs"]=data.tobs
        temp_data.append(temp_dict)
    return jsonify(temp_data)

#@app.route("/api/v1.0/<start>")


#@app.route("/api/v1.0/<start>/<end>")




if __name__ == '__main__':
    app.run(debug=True)
