from .Client import Client

clients = []  # Global list to store all clients


class ClientDB:
    @staticmethod
    def add_client(name, age, client_id):
        """Add a new client or return existing one"""
        # Check if client already exists
        existing_client = ClientDB.find_client(client_id)
        if existing_client:
            return existing_client
        
        # Create new client
        client = Client(name, age, client_id)
        clients.append(client)
        return client

    @staticmethod
    def find_client(client_id):
        """Find a client by their ID"""
        for client in clients:
            if client.client_id == client_id:
                return client
        return None

    @staticmethod
    def get_all_clients():
        """Get all clients"""
        return clients

    @staticmethod
    def client_exists(client_id):
        """Check if a client exists"""
        return ClientDB.find_client(client_id) is not None
