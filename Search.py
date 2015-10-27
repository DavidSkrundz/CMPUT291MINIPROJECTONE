import sys
import Util

def flightQuery(database, roundTrip, retDate, depDate, maxConns, source, destination, bystops):
	Util.clear()
	FlightsProto = """
				Select ROW_NUMBER() OVER ({4}),
				Good_Flights.flightno,
				Good_Flights.flightno2,
				Good_Flights.flightno3,
				Good_Flights.dep_date,
				Good_Flights.dep_date2,
				Good_Flights.dep_date3,
				Good_Flights.fare,
				Good_Flights.fare2,
				Good_Flights.fare3,
				Good_Flights.src,
				Good_Flights.dst,
				Good_Flights.dep_time,
				Good_Flights.arr_time,
				Good_Flights.Stops,
				cast ((Good_Flights.LayoverTime * 60) as decimal(18, 3)),
				cast ((Good_Flights.LayoverTime2 * 60) as decimal(18, 3)),
				Good_Flights.price,
				Good_Flights.seatCount
				from Good_Flights
				where src = '{0}' and
				dst = '{1}' and
				stops <= {2} and
				dep_date = to_date('{3}', 'yyyy-mm-dd')
				{4}
				"""
	flightslist = []

	if bystops:
		there = FlightsProto.format(source, destination, maxConns, depDate, "order by stops, price")
	else:
		there = FlightsProto.format(source, destination, maxConns, depDate, "order by price")

	result = database.get(there)
	Util.print_table(["Row #", "Flight # 1", "Flight # 2", "Flight # 3", "Source", "Destination", "Departure Time", "Arrival Time", "Stops", "Layover 1", "Layover 2", "Price", "Seats"], \
					 [6, 12,12,12,10,11,20,20,10,10,10,10,10], \
					 result,
					 [0, 1 ,2 ,3 ,10,11,12,13,14,15,16,17,18])

	flight = int(input("Choose your flight (by Row #): "))

	stillAvailable = """Select * from Good_Flights where flightno = '{0}'
						AND '{1}' = COALESCE(FLIGHTNO2, 'None')
						AND '{2}' = COALESCE(FLIGHTNO3, 'None')
						AND '{3}' = fare
						AND '{4}' = COALESCE(FARE2, 'None')
						AND '{5}' = COALESCE(FARE3, 'None')
						AND '{6}' = to_char(dep_date, 'yyyy-mm-dd hh24:mi:ss')
						AND '{7}' = COALESCE(TO_CHAR(DEP_DATE2, 'yyyy-mm-dd hh24:mi:ss'), 'None')
						AND '{8}' = COALESCE(TO_CHAR(DEP_DATE3, 'yyyy-mm-dd hh24:mi:ss'), 'None')
						"""

	thereAvailable = stillAvailable.format(result[flight - 1][1], result[flight - 1][2], result[flight - 1][3], \
									result[flight - 1][7], result[flight - 1][8], result[flight - 1][9], \
									str(result[flight - 1][4]), str(result[flight - 1][5]), str(result[flight - 1][6]))

	if (len(database.get(thereAvailable)) > 0):
		flightslist.append(result[flight - 1])
	else:
		return None
	Util.clear()

	if roundTrip:
		if bystops:
			back = FlightsProto.format(destination,source,  maxConns, retDate,  " order by stops, price")
		else:
			back = FlightsProto.format(destination, source,  maxConns, retDate, "order by price")

		resultback = database.get(back)
		Util.print_table(["Row #", "Flight # 1", "Flight # 2", "Flight # 3", "Source", "Destination", "Departure Time", "Arrival Time", "Stops", "Layover 1", "Layover 2", "Price", "Seats"], \
						 [6, 12,12,12,10,11,20,20,10,10,10,10,10], \
						 resultback,
						 [0, 1 ,2 ,3 ,10,11,12,13,14,15,16,17,18])
		flightback = int(input("Choose your return flight (by Row #): "))

		backAvailable = stillAvailable.format(resultback[flight - 1][1], resultback[flight - 1][2], resultback[flight - 1][3], \
										resultback[flight - 1][7], resultback[flight - 1][8], resultback[flight - 1][9], \
										str(resultback[flight - 1][4]), str(resultback[flight - 1][5]), str(resultback[flight - 1][6]))
		if (len(database.get(backAvailable)) > 0):
			flightslist.append(resultback[flightback - 1])
			return flightslist
		else:
			return None

	input("")
