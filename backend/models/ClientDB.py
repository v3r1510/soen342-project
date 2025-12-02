from .Client import Client
from .Database import Database

class ClientDB:
    @staticmethod
    def add_client(name, age, client_id):
        existing_client = ClientDB.find_client(client_id)
        if existing_client:
            return existing_client

        query = "INSERT INTO Client (client_id, name, age) VALUES (?, ?, ?)"
        Database.execute_query(query, (client_id, name, age))

        return Client(name, age, client_id)

    @staticmethod
    def find_client(client_id):
        query = "SELECT client_id, name, age FROM Client WHERE client_id = ?"
        result = Database.execute_query(query, (client_id,), fetch_one=True)
        
        if result:
            return Client(result[1], result[2], result[0])
        return None

    @staticmethod
    def get_all_clients():
        query = "SELECT client_id, name, age FROM Client"
        results = Database.execute_query(query, fetch_all=True)
        
        if results:
            return [Client(row[1], row[2], row[0]) for row in results]
        return []

    @staticmethod
    def client_exists(client_id):

        return ClientDB.find_client(client_id) is not None
