import sys
import Database

def recordDeparture(database, flightno, time):
	query = """UPDATE sch_flights
			SET act_dep_time = TO_DATE({0})
			WHERE flightno = {1}""".format(time, flightno)
			
	database.cursor.execute(query)
	database.commit()

def recordArrival(database, flightno, time):
	query = """UPDATE sch_flights
			SET act_arr_time = TO_DATE({0})
			WHERE flightno = {1}""".format(time, flightno)
			
	database.cursor.execute(query)
	database.commit()