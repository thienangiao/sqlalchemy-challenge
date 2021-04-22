import numpy as np
import datetime as dt

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify


#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite", echo=False)

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Assign the measurement class to a variable called `measure`
Measure = Base.classes.measurement

# Assign the station class to a variable called `Station`
Station = Base.classes.station

#################################################
# Flask Setup
#################################################
app = Flask(__name__)


#################################################
# Flask Routes
#################################################

@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs"
        f"/api/v1.0/<start>"
    )


@app.route("/api/v1.0/precipitation")
def precipitation():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a dictionary of date and precipitation values"""
    # Query
    from_dt=dt.date(2017, 8, 23) - dt.timedelta(days=365)
    results = session.query(Measure.date,Measure.prcp).filter(Measure.date >= from_dt).filter(Measure.prcp != None).order_by(Measure.date).all()

    session.close()

    # Create a dictionary from the row data and append to a list of all_precipitation
    all_precipitation = []
    for date, pcrt in results:
        precipitation_dict = {date:pcrt}
        all_precipitation.append(precipitation_dict)

    return jsonify(all_precipitation)


@app.route("/api/v1.0/stations")
def stations():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of all the stations"""
    # Query all stations
    results = session.query(Station.station).all()

    session.close()

    # Convert list of tuples into normal list
    all_stations = list(np.ravel(results))

    return jsonify(all_stations)


@app.route("/api/v1.0/tobs")
def tobs():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Returns previous year temparature of the current active station"""
    # Query active station in last year of data
    from_dt=dt.date(2017, 8, 23) - dt.timedelta(days=365)

    results = session.query(Measure.station,Measure.date,Measure.tobs).\
            filter(Measure.date >= from_dt).\
            filter(Measure.station == 'USC00519281').\
            filter(Measure.tobs != None).order_by(Measure.date).all()
    session.close()

    # Convert list of tuples into normal list
    active_stations = list(np.ravel(results))

    return jsonify(active_stations)

@app.route("/api/v1.0/<start>")
def tobs(start_date):
    """Fetch data that matches
       the path variable supplied by the user, or a 404 if not."""

    search_dt = start_date.replace(" ", "").lower()
    for temp in justice_league_members:
        search_term = character["real_name"].replace(" ", "").lower()

        if search_term == search_dt:
            return jsonify(character)

    return jsonify({"error": f"{start_date} data not found."}), 404



if __name__ == '__main__':
    app.run(debug=True)
