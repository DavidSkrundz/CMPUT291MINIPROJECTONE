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
		database.put("drop view available_flights")
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
	print("1")
	GoodConns = """
				create view good_1_connections as (
				select a1.src,
				a2.dst,
				a1.dep_date,
				a2.dep_date as dep_date2,
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
				a2.dep_date,
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
	good_1_connections = database.get("Select view_name from all_views where lower(view_name) = 'good_1_connections'")
	if len(good_1_connections) != 0:
		database.put("Drop view good_1_connections")
	database.put(GoodConns)
	print("2")
	#Needs testing
	good2Conns = """
	create view good_2_connections as (
	select a1.src,
	a3.dst,
	a1.dep_date,
	a2.dep_date as dep_date2,
	a3.dep_date as dep_date3,
	a1.dep_time,
	a3.arr_time,
	a1.flightno as flightno1,
	a2.flightno as flightno2,
	a3.flightno as flightno3,
	a2.dep_time-a1.arr_time as layovertime1,
	a3.dep_time -a2.arr_time as layovertime2,
	min(a1.price+a2.price + a3.price) as Price,
	CASE WHEN a1.seats <= a2.seats then (CASE WHEN a1.seats <= a3.seats then a1.seats else a3.seats end) else a2.seats end as seats,
	a1.fare as fare1,
	a2.fare as fare2,
	a3.fare as fare3

	from available_flights a1,
	available_flights a2,
	available_flights a3

	where a1.dst=a2.src and
	a1.arr_time +1.5/24 <=a2.dep_time and
	a1.arr_time +5/24 >=a2.dep_time and
	a2.dst = a3.src and
	a2.arr_time + 1.5/24 <= a3.dep_time and
	a2.arr_time + 5/24 >= a3.dep_time

	group by a1.src,
	a3.dst,
	a1.dep_date,
	a3.dep_date,
	a2.dep_date,
	a1.dep_time,
	a3.arr_time,
	a1.flightno,
	a2.flightno,
	a3.flightno,
	a2.dep_time,
	a1.arr_time,
	a3.dep_time,
	a2.arr_time,
	CASE WHEN a1.seats <= a2.seats then (CASE WHEN a1.seats <= a3.seats then a1.seats else a3.seats end) else a2.seats end,
	a1.fare,
	a2.fare,
	a3.fare)
				 """

	good_2_connections = database.get("Select view_name from all_views where lower(view_name) = 'good_2_connections'")

	if len(good_2_connections) != 0 :
		database.put("drop view good_2_connections")
	database.put(good2Conns)
	print("3")
	#Gonna need to update this to include 2 conns
	GoodFlights =   """
					create view good_flights as (
					Select flightno,
					null as flightno2,
					null as flightno3,
					dep_date,
					null as dep_date2,
					null as dep_date3,
					fare,
					null as fare2,
					null as fare3,
					src,
					dst,
					dep_time,
					arr_time,
					0 as Stops,
					null as LayoverTime,
					null as layovertime2,
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
					seats,
					fare

					UNION

					Select flightno1,
					flightno2,
					null as flightno3,
					dep_date,
					dep_date2,
					null,
					fare1,
					fare2,
					null as fare3,
					src,
					dst,
					dep_time,
					arr_time,
					1 as Stops,
					layovertime,
					null as layovertime2,
					price,
					seats

					from good_1_connections

					UNION

					Select flightno1,
					flightno2,
					flightno3,
					dep_date,
					dep_date2,
					dep_date3,
					fare1,
					fare2,
					fare3,
					src,
					dst,
					dep_time,
					arr_time,
					2 as Stops,
					layovertime1,
					layovertime2,
					price,
					seats

					from good_2_connections
					)
					"""
	good_flights = database.get("Select view_name from all_views where lower(view_name) = 'good_flights'")
	if len(good_flights) != 0:
		database.put("Drop view good_flights")
	database.put(GoodFlights)


def print_table(headings, table_format, data, columns=[]):
    """
    Prints a generic set of data in a tabular format
    Arguments:
    headings: list of heading strings for each column
    table_format: list of character lengths for each column
    columns: column indexes to print
    data: data to tabulate in the form [][], [](), ()()
    Raises:
    ValueError: if the headings, table_format, or data lengths are not compatible
    """
    if not ((len(headings) == len(table_format)) and
            (not columns or (len(table_format) == len(columns)))):
        raise(ValueError("Argument lengths are not compatible."))

    if not columns:
        columns = [i for i in range(len(headings))]

    string_format = ""
    for rule in table_format:
        string_format += "{:<" + str(rule) + "} "

    string_format.strip()

    for row in enumerate(data):
        if (row[0] % 15 == 0):
            print()
            print(string_format.format(*headings))
            print(string_format.replace("{:<", "{:-<").format(*["" for i in range(len(headings))]))
        print(string_format.format(*[str(row[1][i]).strip() for i in columns]))
    print()
