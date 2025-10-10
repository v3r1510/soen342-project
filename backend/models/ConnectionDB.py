from Connection import Connection

connections = []


class ConnectionDB:
    @staticmethod
    def add_connection(self, connection):
        if not isinstance(connection, Connection):
            return False
        else:
            if connection not in connections:
                connections.append(connection)
                return True
            else:
                return False

    @staticmethod
    def find_departure_time(self, connection):
        same_departure = []
        for i in connections:
            if i.compare_departure_time(connection):
                same_departure.append(i)

        return same_departure

    @staticmethod
    def find_arrival_time(self, connection):
        same_arrival = []
        for i in connections:
            if i.compare_arrival_time(connection):
                same_arrival.append(i)

        return same_arrival

    @staticmethod
    def find_departure_city(self, connection):
        same_departure = []
        for i in connections:
            if i.compare_departure_city(connection):
                same_departure.append(i)
        return same_departure

    @staticmethod
    def find_arrival_city(self, connection):
        same_arrival = []
        for i in connections:
            if i.compare_arrival_city(connection):
                same_arrival.append(i)
        return same_arrival

    @staticmethod
    def find_trip_time(self, connection):
        same_trip_time = []
        for i in connections:
            if i.compare_trip_time(connection):
                same_trip_time.append(i)
        return same_trip_time

    @staticmethod
    def find_train_type(self, connection):
        same_train_type = []
        for i in connections:
            if i.compare_train_type(connection):
                same_train_type.append(i)
        return same_train_type

    @staticmethod
    def find_day_of_operation(self, connection):
        same_day_of_operation = []
        for i in connections:
            if i.compare_days_of_operation(connection):
                same_day_of_operation.append(i)
        return same_day_of_operation

    @staticmethod
    def find_first_class_fare(self, connection):
        same_first_class_fare = []
        for i in connections:
            if i.compare_first_class_rate(connection):
                same_first_class_fare.append(i)
        return same_first_class_fare

    @staticmethod
    def find_second_class_fare(self, connection):
        same_second_class_fare = []
        for i in connections:
            if i.compare_second_class_rate(connection):
                same_second_class_fare.append(i)
        return same_second_class_fare

    pass
