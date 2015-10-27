def newTicket(database, email, price):
	query = """SELECT COUNT(*) FROM
		tickets t
		"""
	tno = database.get(query)[0][0]

	name = input("What is your name? ")

	passenger = database.get("""
		select * from passengers p where p.email = '{}' and p.name = '{}'
	""".format(email, name))

	if len(passenger) == 0:
		country = input("What is your country? ")
		database.put("insert into passengers values ('{}', '{}', '{}')".format(email, name, country))

	database.put("insert into tickets values ({}, '{}', '{}', {})".format(tno, email, name, price))
	database.commit()

	return tno
