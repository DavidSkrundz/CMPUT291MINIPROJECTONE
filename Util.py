import os

def findAirportCode(database, airportCodeOrName):
	# Look for airport code
	foundCodes = database.get("select a.acode from airports a where lower(a.acode) = '{}'".format(airportCodeOrName.lower()))
	if len(foundCodes) == 1:
		return foundCodes[0][0]
	else:
		foundCodes = database.get("select a.acode, a.name, a.city from airports a where lower(a.city) like '%{0}%' or lower(a.name) like '%{0}%'".format(airportCodeOrName.lower()))
		if len(foundCodes) > 1:
			print("Multiple matches. Please choose one.")
			for index, code in enumerate(foundCodes):
				print(str(index) + ". " + code[0] + " - " + code[1] + " - " + code[2])
			index = input("Selection #: ")
			return foundCodes[int(index)][0]
		elif len(foundCodes) == 1:
			return foundCodes[0][0]
		else:
			print("BAD THING")
			pass

def clear():
	if os.name == 'nt':
		os.system('cls')
	else:
		os.system('clear')

def setupViews(database):
	availableFlights = database.get("Select view_name from all_views where lower(view_name) = 'available_flights'")
	if len(availableFlights) != 0:
		database.put("drop view available_flights;")
	AvailFlights = """Create view available_flights as (
							select f.flightno,
							sf.dep_date,
							f.src,
							f.dst,
							f.dep_time+(trunc(sf.dep_date)-trunc(f.dep_time)) as Dep_Time,
							f.dep_time+(trunc(sf.dep_date)-trunc(f.dep_time))+(f.est_dur/60+a2.tzone-a1.tzone)/24 as arr_Time,
							fa.fare,
							fa.limit-count(tno) as seats,
							fa.price

							from flights f,
							flight_fares fa,
							sch_flights sf,
							bookings b,
							airports a1,
							airports a2

							where f.flightno=sf.flightno and
							f.flightno=fa.flightno and
							f.src=a1.acode and
							f.dst=a2.acode and
							fa.flightno=b.flightno(+) and
							fa.fare=b.fare(+) and
							sf.dep_date=b.dep_date(+)

							group by f.flightno,
							sf.dep_date,
							f.src,
							f.dst,
							f.dep_time,
							f.est_dur,
							a2.tzone,
							a1.tzone,
							fa.fare,
							fa.limit,
							fa.price
							having fa.limit-count(tno) >= 1)"""
	database.put(AvailFlights)

	GoodConns = """
				create view good_connections as (
				select a1.src,
				a2.dst,
				a1.dep_date,
				a1.dep_time,
				a2.arr_time,
				a1.flightno as flightno1,
				a2.flightno as flightno2,
				a2.dep_time-a1.arr_time as layovertime,
				min(a1.price+a2.price) as Price,
				CASE WHEN a1.seats <= a2.seats then a1.seats else a2.seats end as seats,
				a1.fare as fare1,
				a2.fare as fare2

				from available_flights a1,
				available_flights a2

				where a1.dst=a2.src and
				a1.arr_time +1.5/24 <=a2.dep_time and
				a1.arr_time +5/24 >=a2.dep_time

				group by a1.src,
				a2.dst,
				a1.dep_date,
				a1.dep_time,
				a2.arr_time,
				a1.flightno,
				a2.flightno,
				a2.dep_time,
				a1.arr_time,
				CASE WHEN a1.seats <= a2.seats then a1.seats else a2.seats end,
				a1.fare,
				a2.fare)
				"""
	good_connections = database.get("Select view_name from all_views where lower(view_name) = 'good_connections'")
	if len(good_connections) != 0:
		database.put("Drop view good_connections")
	database.put(GoodConns)

	GoodFlights =   """
					create view good_flights as (
					Select flightno,
					null as flightno2,
					src,
					dst,
					dep_date,
					dep_time,
					arr_time,
					0 as Stops,
					null as LayoverTime,
					price,
					sum(seats) as seatCount,
					fare,
					null as fare2

					From available_flights

					GROUP BY flightno,
					src,
					dst,
					dep_date,
					dep_time,
					arr_time,
					price,
					seats,
					fare

					UNION

					Select flightno1,
					flightno2,
					src,
					dst,
					dep_date,
					dep_time,
					arr_time,
					1 as Stops,
					layovertime,
					price,
					seats,
					fare1,
					fare2

					from good_connections
					)
					"""
	good_flights = database.get("Select view_name from all_views where lower(view_name) = 'good_flights'")
	if len(good_flights) != 0:
		database.put("Drop view good_flights")
	database.put(GoodFlights)
