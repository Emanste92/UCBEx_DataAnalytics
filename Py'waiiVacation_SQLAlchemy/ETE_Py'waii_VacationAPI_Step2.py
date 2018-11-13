# Py'waii Vacation Flask API

# 1. Loading packages, setting up Flask
import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify
app = Flask(__name__)


# 2. Defining precipitation dictionary

precipitation_dict = {
    {
        date:
        prcp: 
    }
}


# 3. Flask routes

# Home
@app.route("/")
def home():
    return (
        f"Py'waii Vacation Flask API<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations"
        f"/api/v1.0/tobs"
        f"/api/v1.0/<start>"
        f"/api/v1.0/<start>/<end>"
    )

# Precipitation 
@app.route("/api/v1.0/precipitation")
def prcps():
    print("Server received request for 'precipitation' page...")
    return jsonify(precipitation_dict)

# Stations
@app.route("/api/v1.0/stations")
def stations():
    print("Server received request for 'stations' page...")
    return 

# Temperature Observations (tobs)
@app.route("/api/v1.0/tobs")
def tobs():
    print("Server received request for 'tobs' page...")
    return 

# Start Temperature Data
@app.route("/api/v1.0/<start>")
def start_temps():
    print("Server received request for 'Start Temperatures' page...")
    return 

# Start/End Temperature Data
@app.route("/api/v1.0/<start>/<end>")
def start_end_temps():
    print("Server received request for 'Start End Temperatures' page...")
    return 

if __name__ == '__main__':
    app.run(debug=True)
