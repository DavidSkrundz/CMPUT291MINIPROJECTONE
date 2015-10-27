import random

def bookingQuery(database, email):
	query = """SELECT t.name, t.paid_price, b.* FROM
			bookings b, tickets t WHERE
			t.tno = b.tno AND
			t.email = '{}'""".format(email)

	database.cursor.execute(query)

def addBooking(database, tno, flightnos, fares, dep_dates):
	seat = str(random.randint(0, 99)) + random.choice("abcdef")
	
	i = 0
	for (flightno in flightnos):
		if flightno == None:
			continue
		else:
			fare = fares[i]
			dep_date = dep_dates[i]
			query = """INSERT INTO bookings
			VALUES({0}, '{1}', '{2}', TO_DATE('{3}', 'YYYY-MM-DD'), '{4}')""".format(
				tno, flightno, fare, dep_date, seat)

			database.cursor.execute(query)
			database.commit()
		i += 1


def cancelBooking(database, tno):
	query = """DELETE FROM
			bookings b WHERE
			b.tno = {}""".format(tno)

	database.cursor.execute(query)
	database.commit()
