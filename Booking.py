import random

def bookingQuery(database, email):
	query = """SELECT ROW_NUMBER() OVER (ORDER BY b.TNO),
			t.name,
			t.paid_price,
			b.tno,
			b.flightno,
			b.fare,
			to_char(b.dep_date, 'yyyy-mm-dd'),
			b.seat
			FROM bookings b, tickets t WHERE
			t.tno = b.tno AND
			t.email = '{}'
			ORDER BY TNO""".format(email)

	database.cursor.execute(query)

def addBooking(database, tno, flightnos, fares, dep_dates):
	seat = str(random.randint(0, 99)) + random.choice("abcdef")

	i = 0
	for flightno in flightnos:
		if flightno == None:
			continue
		else:
			fare = fares[i]
			dep_date = dep_dates[i]
			query = """INSERT INTO bookings
			VALUES({0}, '{1}', '{2}', TO_DATE('{3}', 'YYYY-MM-DD'), '{4}')""".format(
				tno, flightno, fare, dep_date.strftime('%Y-%m-%d'), seat)

			database.cursor.execute(query)
			database.commit()
		i += 1


def cancelBooking(database, tno, flightno, dep_date):
	query = """DELETE FROM
			bookings b WHERE
			b.tno = {0} and
			b.flightno = '{1}' and
			b.dep_date = to_date('{2}', 'yyyy-mm-dd')""".format(tno, flightno, dep_date)

	database.cursor.execute(query)
	database.commit()
