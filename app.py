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

def toDate(dateString): 
    return dt.datetime.strptime(dateString, "%Y-%m-%d").date()

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
        f"/api/v1.0/tobs<br/>"
        f"<br/>"
        f"<br/>"
        f"Route with a start date:<br/>"
        f"/api/v1.0/start_date/yyyy-mm-dd<start>"
        f"<br/>"
        f"<br/>"
        f"Route with a start date and end date:<br/>"
        f"/api/v1.0/start_end_date/yyyy-mm-dd,yyyy-mm-dd<start><end>"
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


@app.route("/api/v1.0/start_date/<start>")

def start(start): 

    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a dictionary of date and precipitation values"""
    # Query
    from_dt=toDate(start)
    results = session.query(func.min(Measure.tobs),func.max(Measure.tobs),func.avg(Measure.tobs)).\
            filter(Measure.date >= from_dt).filter(Measure.tobs != None).all()

    session.close()

       # Create a dictionary from the row data and append to a list of all_precipitation
    stats = []
    for tmin, tmax, tavg in results:
        stats_dict = {"Minimum Temp":tmin,"Maximum Temp":tmax,"Average Temp":tavg}
        stats.append(stats_dict)

    return jsonify(stats)


@app.route("/api/v1.0/start_end_date/<start>,<end>")

def start_end(start,end): 

    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a dictionary of date and precipitation values"""
    # Query
    from_dt=toDate(start)
    to_dt=toDate(end)
    results = session.query(func.min(Measure.tobs),func.max(Measure.tobs),func.avg(Measure.tobs)).\
            filter(Measure.date >= from_dt).filter(Measure.date <= to_dt).filter(Measure.tobs != None).all()

    session.close()

       # Create a dictionary from the row data and append to a list of all_precipitation
    stats = []
    for tmin, tmax, tavg in results:
        stats_dict = {"Minimum Temp":tmin,"Maximum Temp":tmax,"Average Temp":tavg}
        stats.append(stats_dict)

    return jsonify(stats)

    
if __name__ == '__main__':
    app.run(debug=True)
