import sys
import Database

def bookingQuery(database, email):
	query = """SELECT b.tno, t.name, b.dep_date, t.paid_price FROM
			bookings b, tickets t WHERE
			t.tno = b.tno AND
			t.email = '{}'""".format(email)
	
	database.cursor.execute(query)

def cancelBooking(database, tno):
	query = """DELETE FROM
			bookings b WHERE
			b.tno = '{}'""".format(tno)
	
	database.cursor.execute(query)
	database.commit()
			