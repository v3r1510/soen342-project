class Client:
    def __init__(self, name, age, client_id):
        self.name = name
        self.age = age
        self.client_id = client_id  # Generic ID (state-id or passport number)

    def __str__(self):
        return f"{self.name} (ID: {self.client_id})"

    def __eq__(self, other):
        if not isinstance(other, Client):
            return False
        return self.client_id == other.client_id

    def __hash__(self):
        return hash(self.client_id)

    def to_json(self):
        return {
            "name": self.name,
            "age": self.age,
            "client_id": self.client_id
        }
