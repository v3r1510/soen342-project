from .ClientDB import ClientDB
from .ConnectionDB import ConnectionDB
from .Database import Database
from .Reservation import Reservation
from .Trip import Trip

class ReservationDB:
    @staticmethod
    def add_reservation(trip, reservation):
        if not isinstance(trip, Trip) or not isinstance(reservation, Reservation):
            raise TypeError("add_reservation expects a Trip and a Reservation")

        query = """INSERT INTO Reservations (trip_id, client_id, route_id, date_of_reservation, travel_class, ticket_id)
                   VALUES (?, ?, ?, ?, ?, ?)"""
        Database.execute_query(
            query,
            (
                trip.trip_id,
                reservation.client.client_id,
                trip.connection.route_id,
                reservation.date,
                reservation.travel_class,
                reservation.ticket.ticket_id,
            )
        )

    @staticmethod
    def find_reservations_by_client(client_id):
        query = """SELECT reservation_id, trip_id, client_id, route_id, date_of_reservation, travel_class, ticket_id
                   FROM Reservations
                   WHERE client_id = ?"""
        results = Database.execute_query(query, (client_id,), fetch_all=True) or []
        reservations = []
        for row in results:
            connection = ConnectionDB.find_connection_by_route_id(row[3])
            client = ClientDB.find_client(row[2])
            date = row[4]
            travel_class = row[5]
            ticket_id = row[6]

            reservation = Reservation(client, connection, date, travel_class)
            reservation.ticket.ticket_id = ticket_id
            reservations.append(reservation)
        return reservations