import sys
import Database

def bookingQuery(database, email):
	query = """SELECT * FROM
			bookings b, tickets t WHERE
			t.tno = b.tno AND
			t.email = """ + email
	
	database.cursor.execute(query)

def cancelBooking(database, tno):
	query = """
	
			"""
	
	database.cursor.execute(query)
	database.cursor.commit()
			