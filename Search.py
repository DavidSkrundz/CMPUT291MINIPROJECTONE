import sys

def flightQuery(Database, roundTrip, retDate, depDate, partySize, source, destination):

    flightsQ = """SELECT sch_flights.flightno
                    FROM sch_flights INNER JOIN flights
                    ON sch_flights.flightno = flights.flightno
                    WHERE dep_date = '()' AND
                            src = '()' AND
                            dst = '()'"""

    AvailFlights = """select f.flightno,
                            sf.dep_date,
                            f.src,
                            f.dst,
                            f.dep_time+(trunc(sf.dep_date)-trunc(f.dep_time)) as Dep_Time,
	                        f.dep_time+(trunc(sf.dep_date)-trunc(f.dep_time))+(f.est_dur/60+a2.tzone-a1.tzone)/24 as arr_Time,
                            fa.fare,
                            fa.limit-count(tno),
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
                        having fa.limit-count(tno) >= ())""".format(partySize)

    print(AvailFlights)
    thereflights = flightsQ.replace("%DEPDATE", depDate)
    thereflights = thereflights.replace("SOURCE", source)
    thereflights = thereflights.replace("%DESINTATION", destination)

    if roundTrip:
        retflights = flightsQ.replace("%DEPDATE", retDate)
        retflights = retflights.replace("%SOURCE", destination)
        retflights = retflights.replace("%DESTINATION", source)
