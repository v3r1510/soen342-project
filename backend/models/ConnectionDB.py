from .Connection import Connection
from .Database import Database
from .CityDB import CityDB
from .TrainDB import TrainDB

class ConnectionDB:
    @staticmethod
    def add_connection(connection):
        
        if not isinstance(connection, Connection):
            return False
        
        # Check if connection already exists
        query = "SELECT route_id FROM Connections WHERE route_id = ?"
        existing = Database.execute_query(query, (connection.route_id,), fetch_one=True)
        if existing:
            return False
        
        # Insert connection
        query = """
                INSERT INTO Connections
                (route_id, departure_city, arrival_city, departure_time, arrival_time,
                 train_id, days_of_operation, first_class_rate, second_class_rate, trip_time)
                VALUES (?, ?, ?, ?, ?,
                        (SELECT train_id FROM Trains WHERE train_type = ?),
                        ?, ?, ?, ?) 
                """
        params = (
            connection.route_id,
            connection.departure_city.city_name,
            connection.arrival_city.city_name,
            connection.departure_time,
            connection.arrival_time,
            connection.train_type.train_type,
            connection.days_of_operation,
            connection.first_class_rate,
            connection.second_class_rate,
            connection.trip_time
        )
        result = Database.execute_query(query, params)
        return result is not None

    @staticmethod
    def _get_connections_from_rows(rows):
        """Helper method to convert database rows to Connection objects"""
        connections = []
        for row in rows:
            # row: (route_id, departure_city, arrival_city, departure_time, arrival_time,
            #       train_type, days_of_operation, first_class_rate, second_class_rate, trip_time)
            connection = Connection(
                route_id=row[0],
                departure_city=row[1],
                arrival_city=row[2],
                departure_time=row[3],
                arrival_time=row[4],
                train_type=row[5],
                days_of_operation=row[6],
                first_class_rate=row[7],
                second_class_rate=row[8]
            )
            connections.append(connection)
        return connections

    @staticmethod
    def find_departure_time(connection):

        query = """
                SELECT c.route_id,
                       c.departure_city,
                       c.arrival_city,
                       c.departure_time,
                       c.arrival_time,
                       t.train_type,
                       c.days_of_operation,
                       c.first_class_rate,
                       c.second_class_rate,
                       c.trip_time
                FROM Connections c
                         JOIN Trains t ON c.train_id = t.train_id
                WHERE c.departure_time = ? \
                """
        results = Database.execute_query(query, (connection.departure_time,), fetch_all=True)
        return ConnectionDB._get_connections_from_rows(results) if results else []

    @staticmethod
    def find_arrival_time(connection):

        query = """
                SELECT c.route_id,
                       c.departure_city,
                       c.arrival_city,
                       c.departure_time,
                       c.arrival_time,
                       t.train_type,
                       c.days_of_operation,
                       c.first_class_rate,
                       c.second_class_rate,
                       c.trip_time
                FROM Connections c
                         JOIN Trains t ON c.train_id = t.train_id
                WHERE c.arrival_time = ? \
                """
        results = Database.execute_query(query, (connection.arrival_time,), fetch_all=True)
        return ConnectionDB._get_connections_from_rows(results) if results else []

    @staticmethod
    def find_departure_city(connection):
        """Find connections with same departure city"""
        print(connection.departure_city)
        query = """
                SELECT c.route_id,
                       c.departure_city,
                       c.arrival_city,
                       c.departure_time,
                       c.arrival_time,
                       t.train_type,
                       c.days_of_operation,
                       c.first_class_rate,
                       c.second_class_rate,
                       c.trip_time
                FROM Connections c
                         JOIN Trains t ON c.train_id = t.train_id
                WHERE c.departure_city = ? \
                """
        results = Database.execute_query(query, (connection.departure_city.city_name,), fetch_all=True)
        return ConnectionDB._get_connections_from_rows(results) if results else []

    @staticmethod
    def find_arrival_city(connection):

        query = """
                SELECT c.route_id,
                       c.departure_city,
                       c.arrival_city,
                       c.departure_time,
                       c.arrival_time,
                       t.train_type,
                       c.days_of_operation,
                       c.first_class_rate,
                       c.second_class_rate,
                       c.trip_time
                FROM Connections c
                         JOIN Trains t ON c.train_id = t.train_id
                WHERE c.arrival_city = ? \
                """
        results = Database.execute_query(query, (connection.arrival_city.city_name,), fetch_all=True)
        return ConnectionDB._get_connections_from_rows(results) if results else []

    @staticmethod
    def find_trip_time(connection):

        query = """
                SELECT c.route_id,
                       c.departure_city,
                       c.arrival_city,
                       c.departure_time,
                       c.arrival_time,
                       t.train_type,
                       c.days_of_operation,
                       c.first_class_rate,
                       c.second_class_rate,
                       c.trip_time
                FROM Connections c
                         JOIN Trains t ON c.train_id = t.train_id
                WHERE c.trip_time = ? \
                """
        results = Database.execute_query(query, (connection.trip_time,), fetch_all=True)
        return ConnectionDB._get_connections_from_rows(results) if results else []

    @staticmethod
    def find_train_type(connection):

        query = """
                SELECT c.route_id,
                       c.departure_city,
                       c.arrival_city,
                       c.departure_time,
                       c.arrival_time,
                       t.train_type,
                       c.days_of_operation,
                       c.first_class_rate,
                       c.second_class_rate,
                       c.trip_time
                FROM Connections c
                         JOIN Trains t ON c.train_id = t.train_id
                WHERE t.train_type = ? \
                """
        results = Database.execute_query(query, (connection.train_type.train_type,), fetch_all=True)
        return ConnectionDB._get_connections_from_rows(results) if results else []

    @staticmethod
    def find_days_of_operation(connection):

        # Get all connections from database
        query = """
                SELECT c.route_id,
                       c.departure_city,
                       c.arrival_city,
                       c.departure_time,
                       c.arrival_time,
                       t.train_type,
                       c.days_of_operation,
                       c.first_class_rate,
                       c.second_class_rate,
                       c.trip_time
                FROM Connections c
                         JOIN Trains t ON c.train_id = t.train_id \
                """
        results = Database.execute_query(query, fetch_all=True)

        if not results:
            return []

        # Filter using compare_days_of_operation method
        all_connections = ConnectionDB._get_connections_from_rows(results)
        same_day_of_operation = []
        for conn in all_connections:
            if conn.compare_days_of_operation(connection):
                same_day_of_operation.append(conn)

        return same_day_of_operation

    @staticmethod
    def find_first_class_rate(connection):

        query = """
                SELECT c.route_id,
                       c.departure_city,
                       c.arrival_city,
                       c.departure_time,
                       c.arrival_time,
                       t.train_type,
                       c.days_of_operation,
                       c.first_class_rate,
                       c.second_class_rate,
                       c.trip_time
                FROM Connections c
                         JOIN Trains t ON c.train_id = t.train_id
                WHERE c.first_class_rate = ? \
                """
        results = Database.execute_query(query, (int(connection.first_class_rate),), fetch_all=True)
        return ConnectionDB._get_connections_from_rows(results) if results else []

    @staticmethod
    def find_second_class_rate(connection):
        query = """
                SELECT c.route_id,
                       c.departure_city,
                       c.arrival_city,
                       c.departure_time,
                       c.arrival_time,
                       t.train_type,
                       c.days_of_operation,
                       c.first_class_rate,
                       c.second_class_rate,
                       c.trip_time
                FROM Connections c
                         JOIN Trains t ON c.train_id = t.train_id
                WHERE c.second_class_rate = ? \
                """
        results = Database.execute_query(query, (int(connection.second_class_rate),), fetch_all=True)
        return ConnectionDB._get_connections_from_rows(results) if results else []

    @staticmethod
    def get_all_connections():

        query = """
                SELECT c.route_id,
                       c.departure_city,
                       c.arrival_city,
                       c.departure_time,
                       c.arrival_time,
                       t.train_type,
                       c.days_of_operation,
                       c.first_class_rate,
                       c.second_class_rate,
                       c.trip_time
                FROM Connections c
                         JOIN Trains t ON c.train_id = t.train_id \
                """
        results = Database.execute_query(query, fetch_all=True)
        return ConnectionDB._get_connections_from_rows(results) if results else []

    @staticmethod
    def find_connection_by_route_id(route_id):

        query = """
                SELECT c.route_id,
                       c.departure_city,
                       c.arrival_city,
                       c.departure_time,
                       c.arrival_time,
                       t.train_type,
                       c.days_of_operation,
                       c.first_class_rate,
                       c.second_class_rate,
                       c.trip_time
                FROM Connections c
                         JOIN Trains t ON c.train_id = t.train_id
                where c.route_id = ?
                """
        result = Database.execute_query(query, (route_id,), fetch_one=True) or null

        temp_connection = Connection(result[0], result[1],
                                     result[2], result[3], result[4], result[5], result[6],
                                     result[7], result[8])

        return temp_connection
