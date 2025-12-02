from .Database import Database
from .Reservation import Reservation
from .Trip import Trip

class ReservationDB:
    @staticmethod
    def add_reservation(trip, reservation):
        if not isinstance(trip, Trip) or not isinstance(reservation, Reservation):
            raise TypeError("add_reservation expects a Trip and a Reservation")

        query = "INSERT INTO Reservations (trip_id, client_id, route_id)VALUES (?, ?, ?)"
        Database.execute_query(
            query,
            (
                trip.trip_id,
                reservation.client.client_id,
                trip.connection.route_id,
            )
        )

    @staticmethod
    def get_reservations_for_trip(trip_id):
        query = "SELECT reservation_id, trip_id, client_id, route_id FROM Reservation WHERE trip_id = ?"
        rows = Database.execute_query(query, (trip_id,), fetch_all=True) or []
        return rows
