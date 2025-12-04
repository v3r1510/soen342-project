from .Ticket import Ticket


class Reservation:
    def __init__(self, client, connection, date, travel_class):
        self.client = client  # Client object
        self.connection = connection  # Connection object
        self.ticket = Ticket(client, connection)  # Each reservation gets a ticket
        self.date = date
        self.travel_class = travel_class

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
            "connection": self.connection.to_json(),
            "ticket": self.ticket.to_json(),
            "date" : self.date,
            "travel_class": self.travel_class,
            "ticket_id": self.ticket.ticket_id,
        }
