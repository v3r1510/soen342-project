import uuid
from .Reservation import Reservation
from .Ticket import Ticket


class Trip:
    def __init__(self, connection):
        self.trip_id = str(uuid.uuid4())[:8].upper()
        self.connection = connection
        self.reservations = []

    def add_reservation(self, client, date, travel_class):  # Added travel_class parameter
        # Check if client already has a reservation for this connection
        for reservation in self.reservations:
            if reservation.client == client:
                raise ValueError(f"Client {client.name} already has a reservation for this connection")

        # Create reservation with travel_class
        reservation = Reservation(client, self.connection, date, travel_class)
        ticket = Ticket(client, self.connection)
        reservation.ticket = ticket
        self.reservations.append(reservation)
        return reservation

    def get_reservation_count(self):
        """Get total number of reservations in this trip"""
        return len(self.reservations)

    def get_all_tickets(self):
        """Get all tickets for this trip"""
        return [reservation.ticket for reservation in self.reservations]

    def __str__(self):
        return f"Trip {self.trip_id} with {len(self.reservations)} reservation(s)"

    def __eq__(self, other):
        if not isinstance(other, Trip):
            return False
        return self.trip_id == other.trip_id

    def __hash__(self):
        return hash(self.trip_id)

    def to_json(self):
        return {
            "trip_id": self.trip_id,
            "connection": self.connection.to_json(),
            "reservations": [res.to_json() for res in self.reservations],
            "reservation_count": len(self.reservations),
            "tickets": [
                ticket.to_json()
                for ticket in self.get_all_tickets()
                if ticket is not None
            ],
        }
