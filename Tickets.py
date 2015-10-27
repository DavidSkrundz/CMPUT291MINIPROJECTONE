def newTicket(database, email, price):

	name = input("What is your name?: ")

	passenger = database.get("""
		select * from passengers p where p.email = '{}' and p.name = '{}'
	""".format(email, name))

	if len(passenger) == 0:
		country = input("What is your country?: ")
		database.put("insert into passengers values ('{}', '{}', '{}')".format(email, name, country))
		database.commit()

	query = """SELECT max(tno) FROM
		tickets t
		"""
	tno = database.get(query)[0][0] + 1 #You can't be 1 greater than the max unless horrible horrible things happened

	database.put("insert into tickets values ({}, '{}', '{}', {})".format(tno, name, email, price))
	database.commit()

	return tno
