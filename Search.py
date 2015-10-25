import sys

def flightQuery(database, roundTrip, retDate, depDate, maxConns, source, destination, bystops):

	FlightsProto = """
				Select * from GoodFlights
				where src = '{0}' and
				dst = '{1}' and
				stops <= {2}
				dep_date = to_date('{3}', 'yyyy-mm-dd'))
				"""

	if bystops:
		there = FlightsProto.format(source, destination, maxConns, depDate) + "\n order by stops, price"
	else:
		there = FlightsProto.format(source, destination, maxConns, depDate) + "\n order by price"

	theres = database.get(there)
	print("Index    Flight Number  flightno2      Stops     Price     Seats Available")
	for idx, the in enumerate(theres):
		print(str(idx + 1) + '         ' +the[0] +'         ' + str(the[1]) + '           ' + str(the[7]) + '       ' + str(the[9]) + '             ' + str(the[10]))

	flight = int(input("Choose your flight: "))


	stillAvailable = """Select * from GoodFlights where flightno = '{0}' AND
						('{1}' = flightno2 or (flightno2 is null and '{1}' = 'None'))
						AND '{2}' = fare and ('{3}' = fare2 or ( '{3}' = 'None' and fare2 is null))""".format(theres[flight -1][0], theres[flight -1][1], theres[flight -1][11], theres[flight -1][12])

	if len(database.get(stillAvailable)) > 0:
		return theres[flight - 1]
	else:
		return None
	#Not here yet, but we'll eventually get to the point of getting round trips ;)
	print('-----------------------------')

	if roundTrip:
		if bystops:
			back = FlightsProto.format(destination,source,  maxConns, retDate) + "\n order by stops, price"
		else:
			back = FlightsProto.format(destination, source,  maxConns, retDate) + "\n order by price"

		backs = database.get(back)
		for idx, the in enumerate(backs):
			print(str(idx + 1) + ' ' + the[0] + ' ' + str(the[7]) + ' ' + str(the[9]) + ' ' + str(the[10]))




	input("")
