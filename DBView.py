import LoginView

class Session:
	def __init__(self):
		self.agent = False

def DBView(database):
	# First, login
	session = login(database)
	# Some more stuff

def login(database):
	tries = 0
	session = Session()
	while True:
		tries += 1
		(username, password) = LoginView.getLogin("Login into to the database", tries > 1)
		success = database.get("select * from users u where u.email = %s and u.pass = %s", [username, password])
		if success:
			return session

"""
select
	*
from
	thing
where
	something
"""

"""
airports(acode, name, city, country, tzone)
flights(flightno, src, dst, dep_time, est_dur)
sch_flights(flightno, dep_date, act_dep_time, act_arr_time)
fares(fare, descr)
flight_fares(flightno, fare, limit, price, bag_allow)
users(email, pass, last_login)
passengers(email, name, country)
tickets(tno, name, email, paid_price)
bookings(tno, flightno, fare, dep_date, seat)
airline_agents(email, name)
"""


"""
1.
Input:
source			- (Code) or (Name or City then display possible airports) case insensitive
destination		- (Code) or (Name or City then display possible airports) case insensitive
departure date	-

Output:
flight number
source airport code
destination airport code
departure time
arrival time
number of stops
layover time for non-direct flights,
price
number of seats at that price

Returns:
all flights between source + destination on date with available seats (direct + 1 connection)

Sould be sorted by based on price (lowest to the highest)
the user should also have the option to sort the result based on the number of connections
(with direct flights listed first) as the primary sort criterion and the price as the
secondary sort criterion.
"""