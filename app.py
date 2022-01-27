# Import dependencies
import datetime as dt
import numpy as np
import pandas as pd

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

# Setting up the Database
engine = create_engine("sqlite:///hawaii.sqlite") # <- this code allows you to access and query our SQLite database file.
Base = automap_base() # <- this code reflects the database into our classes
Base.prepare(engine, reflect=True) # <- this code relfects the tables into SQLAlchemy
# saving our references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station
session = Session(engine) # <- creating a link from Python to our database


# Setting up Flask
# "Instance" is a general term in programming to refer to a singular version of something
# The __name__ variable denotes the name of the function
# Variables with underscores before and after them are called magic methods in Python
app = Flask(__name__)

# Create Flask Routes
# Define the stating point or root
# The foward slash denotates that we want to put our data at the root of our routes
@app.route('/')
# When creating routes, we follow the naming convention /api/v1.0/ followed by the name of the route.
# This convention signifies that this is version 1 of our application 
# Meaning, it can be updated to support future versions of the app as well
def welcome():
    return(
    '''
    Welcome to the Climate Analysis API!
    Available Routes:
    /api/v1.0/precipitation
    /api/v1.0/stations
    /api/v1.0/tobs
    /api/v1.0/temp/start/end
    ''')

# Precipitation Route    
@app.route("/api/v1.0/precipitation")
def precipitation():
    # Calculate the date one year ago from the most recent date in the database
    prev_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    # Write a query to get the date and precipitation for the previous year
    precipitation = session.query(Measurement.date, Measurement.prcp).\
      filter(Measurement.date >= prev_year).all()
    precip = {date: prcp for date, prcp in precipitation}
    return jsonify(precip)

# Stations Route
@app.route("/api/v1.0/Stations")
def stations():
    # create a query that will allow us to get all of the stations in our database
    results = session.query(Station.station).all()
    # start by unraveling our results into a one-dimensional array
    # and convert our unraveled results into a list
    stations = list(np.ravel(results))
    return jsonify(stations=stations)

# Monthly Temperature Route
@app.route("/api/v1.0/tobs")
def temp_monthly():
    # Calculate the date one year ago from the most recent date in the database
    prev_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    # query the primary station for all the temperature observations from the previous year
    results = session.query(Measurement.tobs).\
        filter(Measurement.station == 'USC00519281').\
        filter(Measurement.date >= prev_year).all()
    # unravel the results into a one-dimensional array and convert that array into a list
    temps = list(np.ravel(results))
    return jsonify(temps=temps)

# Statistics Route
@app.route("/api/v1.0/temp/<start>")
@app.route("/api/v1.0/temp/<start>/<end>")
def stats(start=None, end=None):
    # Create a query to select the minimum, average, and maximum temperatures
    sel = [func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)]
    # To determine the starting and ending date, add an if-not statement
    # The asterik next to `sel` indicates there will be multiple results for the query: min, avg, and max
    if not end:
        results = session.query(*sel).\
            filter(Measurement.date >= start).all()
        temps = list(np.ravel(results))
        return jsonify(temps=temps)

    results = session.query(*sel).\
        filter(Measurement.date >= start).\
        filter(Measurement.date <= end).all()
    temps = list(np.ravel(results))
    return jsonify(temps)