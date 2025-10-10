import pandas as pd
from Connection import Connection
from ConnectionDB import ConnectionDB
from CityDB import CityDB
from TrainDB import TrainDB
from CityDB import cities  # Import the global lists
from TrainDB import trains
from ConnectionDB import connections

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