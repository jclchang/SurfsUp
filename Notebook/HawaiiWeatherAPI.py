import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify


#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///..//Resources/hawaii.sqlite")

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
		f"/api/v1.0/<start><br/>"
		f"/api/v1.0/<start>/<end>"
    )


@app.route("/api/v1.0/precipitation")
def precipitation():
	prcpList = session.query(Measurement).filter(Measurement.date >= '2016-08-23').\
			filter(Measurement.date <= '2017-08-23').all()
	
	all_prcp = []
	for prcp in prcpList:
		prcp_dict = {}
		prcp_dict["date"] = prcp.date
		prcp_dict["prcp"] = prcp.prcp
		all_prcp.append(prcp_dict)
		
	return jsonify(all_prcp)
	
@app.route("/api/v1.0/stations")
def stations():
	stationList = session.query(Station).all()
	
	all_stations = []
	for station in stationList:
		station_dict = {}
		station_dict["station"] = station.station
		station_dict["name"] = station.name
		all_stations.append(station_dict)

	return jsonify(all_stations)
	
@app.route("/api/v1.0/tobs")
def tobs():
	tobsList = session.query(Measurement).filter(Measurement.date >= '2016-08-23').\
			filter(Measurement.date <= '2017-08-23').all()
	
	all_tobs = []
	for tobs in tobsList:
		tobs_dict = {}
		tobs_dict["date"] = tobs.date
		tobs_dict["tobs"] = tobs.tobs
		all_tobs.append(tobs_dict)
		
	return jsonify(all_tobs)
	
	
@app.route("/api/v1.0/<start>")
def temp_start (start):
	tempStat = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
				filter(Measurement.date >= start).all()
	
	all_temp = []
	for temp in tempStat:
		temp_dict = {}
		temp_dict["TMIN"] = temp[0]
		temp_dict["TAVG"] = temp[1]
		temp_dict["TMAX"] = temp[2]
		all_temp.append(temp_dict)
		
	return jsonify(all_temp)

	
@app.route("/api/v1.0/<start>/<end>")
def temp_start_end (start, end):
	tempSEStat = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
				filter(Measurement.date >= start).filter(Measurement.date <= end).all()
	
	SE_temp = []
	for temp1 in tempSEStat:
		temp_dict1 = {}
		temp_dict1["TMIN"] = temp1[0]
		temp_dict1["TAVG"] = temp1[1]
		temp_dict1["TMAX"] = temp1[2]
		SE_temp.append(temp_dict1)
		
	return jsonify(SE_temp)
	#return(start)
	
if __name__ == '__main__':
    app.run(debug=True)
