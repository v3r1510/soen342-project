import random

class Ticket:

    def __init__(self, client, connection):
        self.ticket_id = self.generate_ticket_id()
        self.client = client  # Client object
        self.connection = connection  # Connection object

    def generate_ticket_id(self):
        return f"T{random.randint(1000, 9999)}"

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
            "connection": self.connection.to_json(),
        }
