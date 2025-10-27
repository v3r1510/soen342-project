from .Client import Client

clients = []  #list to store all clients (our db)


class ClientDB:
    @staticmethod
    def add_client(name, age, client_id):
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
        for client in clients:
            if client.client_id == client_id:
                return client
        return None

    @staticmethod
    def get_all_clients():
        return clients

    @staticmethod
    def client_exists(client_id):
        return ClientDB.find_client(client_id) is not None
