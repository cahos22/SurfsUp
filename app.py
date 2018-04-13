# 1. import Flask
import datetime as dt
import numpy as np
import pandas as pd

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask, jsonify


#################################################
# Database Setup
#################################################
# Create engine using the `hawaii.sqlite` database file
engine = create_engine("sqlite:///hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Assign the Measurement and Station tables to classes 
Measurement = Base.classes.Measurement
Station = Base.classes.Station

# Create our session (link) from Python to the DB
session = Session(engine)

#################################################
# Flask Setup
#################################################
app = Flask(__name__)


# 3. Define what to do when a user hits the index route
@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Hawaii Climate Analysis API!<br/>"
        f"Avalable Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/temp/start/end"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    #Query for the dates and temperature observations from 
    #the last year.
    results = session.query(Measurement.date, Measurement.tobs).\
    filter(func.strftime("%Y", Measurement.date) == "2017").all()

   #Convert the query results to a Dictionary using date as the key and tobs as the value.
    # Create a dictionary from the row data and append to a list of all_passengers
   
    temperature_dict = {}
    for temp in results:
        temperature_dict["date"] = temp.tobs

    return jsonify(temperature_dict)


# 4. Define what to do when a user hits the /about route
@app.route("/api/v1.0/stations")
def stations():
  #Return a json list of stations from the dataset.
    results = session.query(Station.station, Station.name).all()

    # Convert list of tuples into normal list
    all_stations = list(np.ravel(results))
    return jsonify(all_stations)


@app.route("/api/v1.0/tobs")
def tobs():
    results = session.query(Measurement.tobs).\
    filter(func.strftime("%Y", Measurement.date) == "2017").all()

    # Convert list of tuples into normal list
    result_list = list(np.ravel(results))
    return jsonify(result_list)


# 4. Define what to do when a user hits the /about route
@app.route("/api/v1.0/start")
def about():
    print("Server received request for 'About' page...")
    return "Welcome to my 'About' page!"


if __name__ == "__main__":
    app.run(debug=True)
