import sys

def flightQuery(database, roundTrip, retDate, depDate, partySize, source, destination, bystops):

	AvailFlights = """With available_flights as (
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


	GoodConns = """
				, Good_connections as (
				select a1.src,
				a2.dst,
				a1.dep_date,
				a1.dep_time,
				a2.arr_time,
				a1.flightno as flightno1,
				a2.flightno as flightno2,
				a2.dep_time-a1.arr_time as layovertime,
				min(a1.price+a2.price) as Price,
				CASE WHEN a1.seats <= a2.seats then a1.seats else a2.seats end as seats

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
				CASE WHEN a1.seats <= a2.seats then a1.seats else a2.seats end)
				"""

	GoodFlights =   """
					, GoodFlights as (
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
					sum(seats) as seatCount

					From available_flights

					GROUP BY flightno,
					src,
					dst,
					dep_date,
					dep_time,
					arr_time,
					price,
					seats

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
					seats

					from good_connections
					)
					"""


	FlightsThere = """
				, FlightsThere as (
				Select * from GoodFlights
				where src = '{0}' and
				dst = '{1}' and
				dep_date = to_date('{2}', 'yyyy-mm-dd'))
				"""

	FlightsBack = """
				, FlightsBack as (
				Select * from GoodFlights
				where src = '{0}' and
				dst = '{1}' and
				dep_date = to_date('{2}', 'yyyy-mm-dd'))
				"""



	if bystops:
		there = AvailFlights + GoodConns + GoodFlights + FlightsThere.format(source, destination, depDate) + "Select * from flightsthere order by stops, price"
	else:
		there = AvailFlights + GoodConns + GoodFlights + FlightsThere.format(source, destination, depDate) + "Select * from flightsthere order by price"

	theres = database.get(there)
	print("Index    Flight Number   Stops     Price     Seats Available")
	for idx, the in enumerate(theres):
		print(str(idx + 1) + '         ' +the[0] + '           ' + str(the[7]) + '       ' + str(the[9]) + '             ' + str(the[10]))

	flight = int(input("Choose your flight: "))
	return theres[flight - 1]

	#Not here yet, but we'll eventually get to the point of getting round trips ;)
	print('-----------------------------')


	if roundTrip:
		if bystops:
			back = AvailFlights + GoodConns + GoodFlights + FlightsBack.format(destination, source, retDate) + "Select * from flightsback order by stops, price"
		else:
			back = AvailFlights + GoodConns + GoodFlights + FlightsBack.format(destination, source, retDate) + "Select * from flightsback order by price"

		backs = database.get(back)
		for idx, the in enumerate(backs):
			print(str(idx + 1) + ' ' + the[0] + ' ' + str(the[7]) + ' ' + str(the[9]) + ' ' + str(the[10]))




	input("")
