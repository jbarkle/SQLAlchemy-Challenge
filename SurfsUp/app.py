# Import the dependencies.
from flask import Flask, jsonify
import pandas as pd
import datetime as dt
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
import numpy as np


#################################################
# Database Setup
#################################################

engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()

# reflect the tables
Base.prepare(autoload_with=engine)

# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station

session = Session(engine)

#################################################
# Flask Setup
#################################################

app = Flask(__name__)

# define variables/functions for later use

# defining active stations
active_stations = session.query(Measurement.station, func.count(Measurement.station)).\
            group_by(Measurement.station).order_by(func.count(Measurement.station).\
            desc())
session.close()

# defining end date
def end_date():
    session = Session(engine)
    end_date = session.query(func.max(Measurement.date))[0][0]
    session.close()
    return end_date

# defining start date
def start_date():
    start_date = "2017-08-23"
    start_date = (dt.datetime.strptime(start_date, '%Y-%m-%d') - dt.timedelta(days=365)).strftime('%Y-%m-%d')
    return start_date

# summary statistics variable
summary_stats = [func.min(Measurement.tobs),
                func.avg(Measurement.tobs),
                func.max(Measurement.tobs)]

# defining dictionary for summary statistics route
def summary_stats_dict(summary,start,rand_date):
    list = []
    for min, max, avg in summary:
        dict = {}
        dict["start_date"] = start
        dict["end_date"] = rand_date
        dict["TMIN"] = min
        dict["TAVG"] = avg
        dict["TMAX"] = max
        list.append(dict)
    return list

#################################################
# Flask Routes
#################################################

# create a new route: /
@app.route('/')
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start><br/>"
        f"/api/v1.0/<start>/<end>"
    )
# create a new route: /precipitation
@app.route("/api/v1.0/precipitation")
def precipitation():
    # Create our session (link) from Python to the DB
    session = Session(engine)
    """Return a list of precipitation data including the date"""
    # Query precipitation data
    results = session.query(Measurement.date,Measurement.prcp).\
    filter(Measurement.date <= '2017-08-23').filter(Measurement.date >= '2016-08-23').\
    all()
    session.close()
    # Create a dictionary from the row data and append to a list of precip_data
    precip_data = []
    for date, prcp in results:
        prcp_dict = {}
        prcp_dict["date"] = date
        prcp_dict["precipitation"] = prcp
        precip_data.append(prcp_dict)
    # return data as JSON
    return jsonify(precip_data)

# create a new route: /stations
@app.route("/api/v1.0/stations")
def stations():
    # Create our session (link) from Python to the DB
    session = Session(engine)
    """Return a list of stations data"""
    # Query stations data
    stations_results = session.query(Measurement.station).\
            group_by(Measurement.station).\
            all()
    session.close()
    # convert list to contiguous flattened array
    all_stations = list(np.ravel(stations_results))
    # return data as JSON
    return jsonify(all_stations)

# create a new route: /tobs
@app.route("/api/v1.0/tobs")
def tobs():
    # Create our session (link) from Python to the DB
    session = Session(engine)
    """Return a list of dates and temperature observations of the most-active station for the previous year of data"""
    # Query tobs data
    tobs_results = session.query(Measurement.tobs).\
                filter(Measurement.date >= '2016-08-23').\
                filter(Measurement.station == active_stations[0][0]).\
                all()
    session.close()
    tobservations = list(np.ravel(tobs_results))
    # return data as JSON
    return jsonify(tobservations)

# create a new route: /<start>
@app.route("/api/v1.0/<start>")
def input_start(start):
    # Create our session (link) from Python to the DB
    session = Session(engine)
    # Query start data
    start_results = session.query(*summary_stats)\
                .filter(Measurement.date >= start)
    session.close()
    # return data in JSON
    return jsonify(summary_stats_dict(start_results,start,end_date()))

# create a new route: /<start>/<end>
@app.route("/api/v1.0/<start>/<end>")
def input_start_end(start,end):
    # Create our session (link) from Python to the DB
    session = Session(engine)
    # Query start data
    start_end_results = session.query(*summary_stats)\
                        .filter(Measurement.date >= start)\
                        .filter(Measurement.date <= end)
    session.close()
    # return data in JSON
    return jsonify(summary_stats_dict(start_end_results,start,end))



if __name__ == "__main__":
    app.run(debug=True)