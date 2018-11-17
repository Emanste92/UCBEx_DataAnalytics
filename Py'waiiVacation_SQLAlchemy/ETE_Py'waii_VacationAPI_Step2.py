# Py'waii Vacation Flask API

# 1. Loading packages 
import numpy as np
import datetime as dt
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask, jsonify

# 2. Setting up sqlite session and Flask
engine = create_engine("sqlite:///Resources/hawaii.sqlite")
Base = automap_base()
Base.prepare(engine, reflect=True)
Measurement = Base.classes.measurement
Station = Base.classes.station
session = Session(engine)

app = Flask(__name__)

# 3. Dictionaries of query results from Step1 notebook

# determining the last day of the dataset and the year prior to that date
latest_date_query = str(session.query(Measurement.date).\
                    order_by(Measurement.date.desc()).first())
latest_date = latest_date_query[2:12]
year_before_latest_date_calc = str(int(latest_date[0:4]) - 1)
year_before_latest_date = year_before_latest_date_calc + latest_date[4:]

# precipitation of the last year from the last date in the dataset
prcp_query = session.query(Measurement.date,Measurement.station,Measurement.prcp).\
            filter(Measurement.date.between(year_before_latest_date,latest_date)).\
            order_by(Measurement.date).all()
prcp_year = []
for prcp in prcp_query:
    prcp_dict = {}
    prcp_dict['date'] = prcp.date
    prcp_dict['prcp'] = prcp.prcp
    prcp_dict['station_ID'] = prcp.station
    prcp_year.append(prcp_dict)

# list of weather stations
station_query = session.query(Station.name,Station.station,
                Station.latitude,Station.longitude,Station.elevation).all()
station_names = []
for station in station_query:
    station_dict = {}
    station_dict['name'] = station.name
    station_dict['station_id'] = station.station
    station_names.append(station_dict)

# query of observerd temperatures (tobs) of the last year 
# from the last date in the dataset
tobs_query = session.query(Measurement.date,Measurement.station,Measurement.tobs).\
                    filter(Measurement.date.between(year_before_latest_date,latest_date)).\
                    order_by(Measurement.date).all()
tobs_year = []
for tob in tobs_query:
    tobs_dict = {}
    tobs_dict['date'] = tob.date
    tobs_dict['tobs'] = tob.tobs
    tobs_dict['station_id'] = tob.station
    tobs_year.append(tobs_dict)

# 4. Flask routes

# Home
@app.route("/")
def home():
    return (
        f"Aloha! Welcome to the Py'waii Vacation Flask API!!!<br/>"
        f"<br/>"
        f"Your available basic query routes that will pull all points<br/>"
        f"from the date range 2017-03-05 to 2017-03-17<br/>"
        f"<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"<br/>"
        f"You can also query by a start date or a start/end range<br/>"
        f"using the year-month-day date format<br/>"
        f"<br/>"
        f"Examples:<br/>"
        f"/api/v1.0/2011-06-12<br/>"
        f"This will return the minimum temperature (tmin), max temperature (tmax),<br/>" 
        f"and average temperature (tavg) of all dates greater than and<br/>" 
        f"equal to this start date<br/>"
        f"<br/>"
        f"/api/v1.0/2014-08-01/2014-08-21<br/>"
        f"This will return the minimum temperature (tmin), max temperature (tmax),<br/>" 
        f"and average temperature (tavg) of all dates inclusive<br/>"
        f"between the start and end date<br/>"
    )

# Precipitation 
@app.route("/api/v1.0/precipitation")
def prcps():
    print("Server received request for 'precipitation' page...")
    return jsonify(prcp_year)

# Stations
@app.route("/api/v1.0/stations")
def stations():
    print("Server received request for 'stations' page...")
    return jsonify(station_names)

# Temperature Observations (tobs)
@app.route("/api/v1.0/tobs")
def tobs():
    print("Server received request for 'tobs' page...")
    return jsonify(tobs_year)

# Start Temperature Data: tmin, tmax, tavg for dates greater than and equal to start date
@app.route("/api/v1.0/<start>")
def start(start):
    print("Server received request for 'Start Temperatures' page...")
    start_date = dt.datetime.strptime(start, '%Y-%m-%d')
    # <start> route: tmin, tmax, tavg for dates greater than and equal to the start date input
    # created by running specific queries of the user-provided start date
    tmin_start = session.query(func.min(Measurement.tobs)).filter(Measurement.date >= start_date).scalar()
    tmax_start = session.query(func.max(Measurement.tobs)).filter(Measurement.date >= start_date).scalar()
    tavg_start = session.query(func.round(func.avg(Measurement.tobs))).filter(Measurement.date >= start_date).scalar()
    result = [{"tmin":tmin_start},{"tmax":tmax_start},{"tavg":tavg_start}]
    return jsonify(result)

# Start/End Temperature Data
@app.route("/api/v1.0/<start>/<end>")
def startend(start, end):
    print("Server received request for 'Start End Temperatures' page...")
    start_date = dt.datetime.strptime(start, '%Y-%m-%d')
    end_date = dt.datetime.strptime(end, '%Y-%m-%d')
    # <start>/<end> route: tmin, tmax, tavg for dates between start and end date inclusive
    # created by running specific queries of the user-provided start date and end date  
    tmin_period = session.query(func.min(Measurement.tobs)).filter(Measurement.date.between(start_date, end_date)).scalar()
    tmax_period = session.query(func.max(Measurement.tobs)).filter(Measurement.date.between(start_date, end_date)).scalar()
    tavg_period = session.query(func.round(func.avg(Measurement.tobs))).filter(Measurement.date.between(start_date, end_date)).scalar()
    result = [{"tmin":tmin_period},{"tmax":tmax_period},{"tavg":tavg_period}]
    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True)