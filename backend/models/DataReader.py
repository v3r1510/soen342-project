import pandas as pd
from .Connection import Connection

class DataReader:

    def __init__(self, file_name):
        self.file_name = file_name
        self.df = pd.read_csv(file_name)
        self.return_record_array()
        test = self.return_record_array()


    def read(self):
        self.df = pd.read_csv(self.file_name)

    def return_record_array(self):
        connections = []
        for _, row in self.df.iterrows():
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
            connections.append(connection)
        return connections



    pass