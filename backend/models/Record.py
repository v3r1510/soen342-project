from datetime import datetime, timedelta


class Record:
    def __init__(self, route_id, departure_city, arrival_city, departure_time, arrival_time, train_type, days_of_operation, first_class_rate, second_class_rate):
        self.route_id = route_id
        self.departure_city = departure_city
        self.arrival_city = arrival_city
        self.departure_time = departure_time
        self.arrival_time = arrival_time
        self.train_type = train_type
        self.days_of_operation = days_of_operation
        self.first_class_rate = first_class_rate
        self.second_class_rate = second_class_rate
        self.trip_time = self.calulate_trip_time()

    #calculates the trip time in minutes
    def calulate_trip_time(self):
        format = "%H:%M"
        departure = datetime.strptime(self.departure_time, format)
        arrival = datetime.strptime(self.arrival_time, format)
        if arrival < departure:
            arrival += timedelta(days=1)
        return int((arrival - departure).total_seconds() /60 )

    def to_json(self):
        return {"departure_city": self.departure_city, "arrival_city" : self.arrival_city, "departure_time" : self.departure_time, "arrival_time" : self.arrival_time,
                "train_type" : self.train_type, "days_of_operation" : self.days_of_operation, "first_class_rate" : self.first_class_rate, "second_class_rate" : self.second_class_rate,
                "trip_time" : self.trip_time}

    pass