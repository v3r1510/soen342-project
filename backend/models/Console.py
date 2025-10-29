import pandas as pd
from .Connection import Connection
from .ConnectionDB import ConnectionDB
from .CityDB import CityDB
from .TrainDB import TrainDB
from .CityDB import cities  
from .TrainDB import trains
from .ConnectionDB import connections
from .ClientDB import ClientDB, clients
from .TripDB import TripDB, trips
from .Trip import Trip

class Console:
    def __init__(self, filename):
        self.file_data = pd.DataFrame()
        self.load_records(filename)

    def load_records(self, file_name):
        self.file_data = pd.read_csv(file_name)

        print("loading cities")
        for _, row in self.file_data.iterrows():
            CityDB.add_city(row['Departure City'])
            CityDB.add_city(row['Arrival City'])
            TrainDB.add_train(row['Train Type'])

        print(f"Loaded {len(cities)} cities and {len(trains)} trains")

        print("innitializing connections")
        for _, row in self.file_data.iterrows():
            connection = Connection(
                route_id=row['Route ID'],
                departure_city=row['Departure City'],
                arrival_city=row['Arrival City'],
                departure_time=row['Departure Time'],
                arrival_time=row['Arrival Time'],
                train_type=row['Train Type'],
                days_of_operation=row['Days of Operation'],
                first_class_rate=row['First Class ticket rate (in euro)'],
                second_class_rate=row['Second Class ticket rate (in euro)']
            )
            ConnectionDB.add_connection(connection)

        print(f"Loaded {len(connections)} connections")

    def search_routes(self, departure_city=None, arrival_city=None, departure_time=None, 
                     arrival_time=None, train_type=None, days_of_operation=None, 
                     first_class_rate=None, second_class_rate=None):
        """Search for routes based on criteria"""
        print(departure_city)
        results = []
        user = Connection("U001", departure_city, arrival_city, departure_time, arrival_time,train_type, days_of_operation, first_class_rate, second_class_rate)
        # print((user))
        # print(user.departure_city)
        if departure_city:
            # departure_cities = ConnectionDB.find_departure_city(user)
            results.append(ConnectionDB.find_departure_city(user))
        if arrival_city:
            # arrival_cities = ConnectionDB.find_arrival_city(user)
            results.append(ConnectionDB.find_arrival_city(user))
        if departure_time:
            # departure_times = ConnectionDB.find_departure_time(user)
            results.append(ConnectionDB.find_departure_time(user))
        if arrival_time:
            # arrivale_times = ConnectionDB.find_arrival_time(user)
            results.append(ConnectionDB.find_arrival_time(user))
        if train_type:
            # train_types = ConnectionDB.find_train_type(user)
            results.append(ConnectionDB.find_train_type(user))
        if days_of_operation:
            # days_of_operations = ConnectionDB.find_days_of_operation(user)
            results.append(ConnectionDB.find_days_of_operation(user))
        if first_class_rate:
            # first_classe_rates = ConnectionDB.find_first_class_rate(user)
            results.append(ConnectionDB.find_first_class_rate(user))
        if second_class_rate:
            # second_class_rates = ConnectionDB.find_second_class_rate(user)
            results.append(ConnectionDB.find_second_class_rate(user))

        if not results:
            return []

        return list(set.intersection(*(set(rlts) for rlts in results)))

    def get_all_routes(self):
        """Get all available routes"""
        return connections

    def get_all_cities(self):
        """Get all available cities"""
        return [city.name for city in cities]

    def get_all_train_types(self):
        """Get all available train types"""
        return [train.name for train in trains]

    def routes_to_json(self, routes_list):
        """Convert list of routes to JSON format for frontend"""
        return [route.to_json() for route in routes_list]

    def book_trip(self, travelers, connection):
    
        if not isinstance(connection, Connection):
            raise TypeError("connection must be a Connection object")
        
        if not travelers or len(travelers) == 0:
            raise ValueError("At least one traveler is required")
        
        # Create the trip for this connection
        trip = Trip(connection)
        
        # Add each traveler as a reservation
        for traveler_data in travelers:
            # Get or create client
            client = ClientDB.add_client(
                name=traveler_data['name'],
                age=traveler_data['age'],
                client_id=traveler_data['client_id']
            )
            
            # Add reservation for this client
            try:
                trip.add_reservation(client)
            except ValueError as e:
                # Client already has a reservation for this connection
                raise ValueError(f"Error booking trip: {str(e)}")
        
        # Save trip to database
        TripDB.add_trip(trip)
        
        return trip

    def get_all_clients(self):
        """Get all clients who have made reservations"""
        return clients

    def get_all_trips(self):
        """Get all booked trips"""
        return trips

    def find_trip_by_id(self, trip_id):
        """Find a specific trip by ID"""
        return TripDB.find_trip(trip_id)

    def find_client_trips(self, client_id):
        """Find all trips for a specific client"""
        client = ClientDB.find_client(client_id)
        if not client:
            return []
        return TripDB.find_trips_by_client(client)
