from .Trip import Trip
from .Database import Database
from .ConnectionDB import ConnectionDB

class TripDB:
    @staticmethod
    def add_trip(trip):
        """Add a trip to the database"""
        if not isinstance(trip, Trip):
            raise TypeError("Must provide a Trip object")
        
        # Check if trip already exists
        query = "SELECT trip_id FROM Trips WHERE trip_id = ?"
        existing = Database.execute_query(query, (trip.trip_id,), fetch_one=True)
        if existing:
            return False
        
        # Insert trip
        query = """
            INSERT INTO Trips (trip_id, route_id)
            VALUES (?, ?)
        """
        result = Database.execute_query(query, (trip.trip_id, trip.connection.route_id))
        return result is not None

    @staticmethod
    def find_trip(trip_id):
        """Find a trip by its ID"""
        query = """
            SELECT t.trip_id, c.route_id, c.departure_city, c.arrival_city, 
                   c.departure_time, c.arrival_time, tr.train_type, c.days_of_operation,
                   c.first_class_rate, c.second_class_rate, c.trip_time
            FROM Trips t
            JOIN Connections c ON t.route_id = c.route_id
            JOIN Trains tr ON c.train_id = tr.train_id
            WHERE t.trip_id = ?
        """
        result = Database.execute_query(query, (trip_id,), fetch_one=True)
        
        if result:
            # Create Connection object
            from .Connection import Connection
            connection = Connection(
                route_id=result[1],
                departure_city=result[2],
                arrival_city=result[3],
                departure_time=result[4],
                arrival_time=result[5],
                train_type=result[6],
                days_of_operation=result[7],
                first_class_rate=result[8],
                second_class_rate=result[9]
            )
            # Create Trip object
            trip = Trip(connection)
            trip.trip_id = result[0]  # Override the generated ID with the stored one
            return trip
        return None

    @staticmethod
    def get_all_trips():
        """Get all trips"""
        query = """
            SELECT t.trip_id, c.route_id, c.departure_city, c.arrival_city, 
                   c.departure_time, c.arrival_time, tr.train_type, c.days_of_operation,
                   c.first_class_rate, c.second_class_rate, c.trip_time
            FROM Trips t
            JOIN Connections c ON t.route_id = c.route_id
            JOIN Trains tr ON c.train_id = tr.train_id
        """
        results = Database.execute_query(query, fetch_all=True)
        
        if not results:
            return []
        
        trips = []
        from .Connection import Connection
        for row in results:
            connection = Connection(
                route_id=row[1],
                departure_city=row[2],
                arrival_city=row[3],
                departure_time=row[4],
                arrival_time=row[5],
                train_type=row[6],
                days_of_operation=row[7],
                first_class_rate=row[8],
                second_class_rate=row[9]
            )
            trip = Trip(connection)
            trip.trip_id = row[0]
            trips.append(trip)
        
        return trips

    @staticmethod
    def find_trips_by_client(client):
       
        # Note: This requires querying Reservations table
        # For now, return empty list as Reservations need to be handled separately
        # This will be properly implemented when ReservationDB is updated
        return []
