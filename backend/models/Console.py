import pandas as pd
from .Connection import Connection
from .ConnectionDB import ConnectionDB
from .CityDB import CityDB
from .TrainDB import TrainDB
from .CityDB import cities  # Import the global lists
from .TrainDB import trains
from .ConnectionDB import connections

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
                first_class_rate=row['First Class Rate'],
                second_class_rate=row['Second Class Rate']
            )
            ConnectionDB.add_connection(connection)

        print(f"Loaded {len(connections)} connections")

    def search_routes(self, departure_city=None, arrival_city=None, departure_time=None, 
                     arrival_time=None, train_type=None, days_of_operation=None, 
                     first_class_rate=None, second_class_rate=None):
        """Search for routes based on criteria"""
        results = []
        
        for connection in connections:
            match = True
            
            if departure_city and connection.departure_city.name.lower() != departure_city.lower():
                match = False
            if arrival_city and connection.arrival_city.name.lower() != arrival_city.lower():
                match = False
            if departure_time and connection.departure_time != departure_time:
                match = False
            if arrival_time and connection.arrival_time != arrival_time:
                match = False
            if train_type and connection.train_type.name.lower() != train_type.lower():
                match = False
            if days_of_operation and connection.days_of_operation != days_of_operation:
                match = False
            if first_class_rate and connection.first_class_rate != first_class_rate:
                match = False
            if second_class_rate and connection.second_class_rate != second_class_rate:
                match = False
                
            if match:
                results.append(connection)
        
        return results

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