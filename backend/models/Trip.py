import uuid
from .Reservation import Reservation


class Trip:
    def __init__(self, connection):
        self.trip_id = str(uuid.uuid4())[:8].upper()  
        self.connection = connection 
        self.reservations = []  

    def add_reservation(self, client):
        """
        Add a reservation for a client
        Ensures a client can only have ONE reservation per connection
        """
        # Check if client already has a reservation for this connection
        for reservation in self.reservations:
            if reservation.client == client:
                raise ValueError(f"Client {client.name} already has a reservation for this connection")
        
   
        reservation = Reservation(client, self.connection)
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
            "connection": {
                "route_id": self.connection.route_id,
                "departure_city": self.connection.departure_city.city_name,
                "arrival_city": self.connection.arrival_city.city_name,
                "departure_time": self.connection.departure_time,
                "arrival_time": self.connection.arrival_time,
                "train_type": self.connection.train_type.train_type
            },
            "reservations": [res.to_json() for res in self.reservations],
            "reservation_count": len(self.reservations),
            "tickets": [ticket.to_json() for ticket in self.get_all_tickets()]
        }
