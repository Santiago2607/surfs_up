import datetime as dt
import numpy as np
import pandas as pd
# Let's get the dependencies we need for SQLAlchemy, which will help us access our data in the SQLite database.
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
# Add the code to import the dependencies that we need for Flask
from flask import Flask, jsonify


# We'll set up our database engine for the Flask application
engine = create_engine("sqlite:///hawaii.sqlite")
# Now let's reflect the database into our classes.
Base = automap_base()
# Add the following code to reflect the database:
Base.prepare(engine, reflect=True)
# We'll create a variable for each of the classes so that we can reference them later.
Measurement = Base.classes.measurement
Station = Base.classes.station
# Create a session link from Python to our database with the following code:
session = Session(engine)
# Set Up Flask
# To define our Flask app, add the following line of code. This will create a Flask application called "app."
app = Flask(__name__)
# We can define the welcome route using the code below:
@app.route("/")
# Now our root, or welcome route, is set up. The next step is to add the routing information for each of the other routes.
# First, create a function welcome() with a return statement.
# Next, add the precipitation, stations, tobs, and temp routes that we'll need for this module into our return statement.
def welcome():
    return(
    '''
    Welcome to the Climate Analysis API!
    Available Routes:
    /api/v1.0/precipitation
    /api/v1.0/stations
    /api/v1.0/tobs
    /api/v1.0/temp/start/end
    '''
    )
# Then to run the code we have to go the command line to navigate to your project folder. Then run your code: flask run


# To create the route, add the following code. Make sure that it's aligned all the way to the left.
@app.route("/api/v1.0/precipitation")
# Next, we will create the precipitation() function.
def precipitation():
    prev_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    precipitation=session.query(Measurement.date, Measurement.prcp).\
        filter(Measurement.date >= prev_year).all()
    precip = {date:prcp for date, prcp in precipitation}
    return jsonify(precip)


# We want to start by unraveling our results into a one-dimensional array. To do this, we want to use the function np.ravel(), 
# with results as our parameter.
#Next, we will convert our unraveled results into a list. To convert the results to a list, we will need to use the list function, 
# which is list(), and then convert that array into a list.
@app.route("/api/v1.0/stations")
def stations():
    results = session.query(Station.station).all()
    stations = list(np.ravel(results))
    return jsonify(stations=stations)


# Next route: Temperature Observations
@app.route("/api/v1.0/tobs")
def temp_monthly():
    prev_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    results = session.query(Measurement.tobs).\
      filter(Measurement.station == 'USC00519281').\
      filter(Measurement.date >= prev_year).all()
    temps = list(np.ravel(results))
    return jsonify(temps=temps)


# Final route: Statistics, so the investors can see the minimum, maximum, and average temperatures.
@app.route("/api/v1.0/temp/<start>")
@app.route("/api/v1.0/temp/<start>/<end>")
def stats(start=None, end=None):
    sel = [func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)]

    if not end:
        results = session.query(*sel).\
            filter(Measurement.date >= start).all()
        temps = list(np.ravel(results))
        return jsonify(temps)

    results = session.query(*sel).\
        filter(Measurement.date >= start).\
        filter(Measurement.date <= end).all()
    temps = list(np.ravel(results))
    return jsonify(temps)







