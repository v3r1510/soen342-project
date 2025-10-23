class Ticket:
    _ticket_counter = 1000  # Start ticket IDs from 1000

    def __init__(self, client, connection):
        self.ticket_id = Ticket._ticket_counter
        Ticket._ticket_counter += 1
        self.client = client  # Client object
        self.connection = connection  # Connection object

    def __str__(self):
        return f"Ticket #{self.ticket_id} for {self.client.name}"

    def __eq__(self, other):
        if not isinstance(other, Ticket):
            return False
        return self.ticket_id == other.ticket_id

    def __hash__(self):
        return hash(self.ticket_id)

    def to_json(self):
        return {
            "ticket_id": self.ticket_id,
            "client": self.client.to_json(),
            "connection": {
                "route_id": self.connection.route_id,
                "departure_city": self.connection.departure_city.city_name,
                "arrival_city": self.connection.arrival_city.city_name,
                "departure_time": self.connection.departure_time,
                "arrival_time": self.connection.arrival_time,
                "train_type": self.connection.train_type.train_type
            }
        }
