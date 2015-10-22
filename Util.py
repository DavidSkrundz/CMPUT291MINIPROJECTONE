def findAirportCode(database, airportCodeOrName):
	# Look for airport code
	foundCodes = database.get("select a.acode from airports a where lower(a.acode) = '{}'".format(airportCodeOrName.lower()))
	if foundCodes == 1:
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