from .Ticket import Ticket


class Reservation:
    def __init__(self, client, connection):
        self.client = client  # Client object
        self.connection = connection  # Connection object
        self.ticket = Ticket(client, connection)  # Each reservation gets a ticket

    def __str__(self):
        return f"Reservation for {self.client.name} - {self.ticket}"

    def __eq__(self, other):
        if not isinstance(other, Reservation):
            return False
        # A reservation is unique by client and connection combination
        return self.client == other.client and self.connection == other.connection

    def __hash__(self):
        return hash((self.client, self.connection.route_id))

    def to_json(self):
        return {
            "client": self.client.to_json(),
            "connection": {
                "route_id": self.connection.route_id,
                "departure_city": self.connection.departure_city.city_name,
                "arrival_city": self.connection.arrival_city.city_name,
                "departure_time": self.connection.departure_time,
                "arrival_time": self.connection.arrival_time,
                "train_type": self.connection.train_type.train_type
            },
            "ticket": self.ticket.to_json()
        }
