from .Trip import Trip

trips = []  #list of all the trips (our db) 


class TripDB:
    @staticmethod
    def add_trip(trip):
        """Add a trip to the database"""
        if not isinstance(trip, Trip):
            raise TypeError("Must provide a Trip object")
        
        if trip not in trips:
            trips.append(trip)
            return True
        return False

    @staticmethod
    def find_trip(trip_id):
        """Find a trip by its ID"""
        for trip in trips:
            if trip.trip_id == trip_id:
                return trip
        return None

    @staticmethod
    def get_all_trips():
        """Get all trips"""
        return trips

    @staticmethod
    def find_trips_by_client(client):
        """Find all trips that include a specific client"""
        client_trips = []
        for trip in trips:
            for reservation in trip.reservations:
                if reservation.client == client:
                    client_trips.append(trip)
                    break
        return client_trips
