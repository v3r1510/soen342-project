from datetime import datetime, timedelta
from .CityDB import CityDB
from .TrainDB import TrainDB
from .DayParser import DayParser


class Connection:
    def __init__(self, route_id, departure_city, arrival_city, departure_time, arrival_time, train_type,
                 days_of_operation, first_class_rate, second_class_rate):
        self.route_id = route_id
        self.departure_city = CityDB.find_city(departure_city)
        self.arrival_city = CityDB.find_city(arrival_city)
        self.departure_time = departure_time
        self.arrival_time = arrival_time
        self.train_type = TrainDB.find_train(train_type)
        self.days_of_operation = days_of_operation
        self.first_class_rate = first_class_rate
        self.second_class_rate = second_class_rate
        self.trip_time = self.calulate_trip_time()

    def calulate_trip_time(self):
        if not self.departure_time or not self.arrival_time:
            return 0 
        def parse_time(time_str):
            next_day = False
            if "(+1d)" in time_str:
                next_day = True
                time_str = time_str.replace("(+1d)", "").strip()

            formats = [
                "%H:%M:%S",
                "%H:%M",
                "%I:%M:%S %p",
                "%I:%M %p",
            ]
            for fmt in formats:
                try:
                    dt = datetime.strptime(time_str, fmt)
                    if next_day:
                        dt += timedelta(days=1)
                    return dt
                except ValueError:
                    continue
            raise ValueError(f"Time format not recognized: {time_str}")

        departure = parse_time(self.departure_time)
        arrival = parse_time(self.arrival_time)

        return int((arrival - departure).total_seconds() / 60)

    def to_json(self):
        return {"departure_city": str(self.departure_city), "arrival_city": str(self.arrival_city),
                "departure_time": self.departure_time, "arrival_time": self.arrival_time,
                "train_type": str(self.train_type), "days_of_operation": self.days_of_operation,
                "first_class_rate": str(self.first_class_rate), "second_class_rate": str(self.second_class_rate),
                "trip_time": str(self.trip_time)}

    def _key(self):
        return (
            self.departure_city,
            self.arrival_city,
            self.departure_time,
            self.arrival_time,
            self.train_type,
            self.days_of_operation,
            self.first_class_rate,
            self.second_class_rate,
            self.trip_time,
        )

    def __eq__(self, other):
        if not isinstance(other, Connection):
            return NotImplemented
        return self._key() == other._key()

    def __hash__(self):
        return hash(self._key())

    def compare_departure_time(self, other):
        if not isinstance(other, Connection):
            return False
        return self.departure_time == other.departure_time

    def compare_arrival_time(self, other):
        if not isinstance(other, Connection):
            return False
        return self.arrival_time == other.arrival_time

    def compare_trip_time(self, other):
        if not isinstance(other, Connection):
            return False
        return self.trip_time == other.trip_time

    def compare_departure_city(self, other):
        if not isinstance(other, Connection):
            return False
        return self.departure_city == other.departure_city

    def compare_arrival_city(self, other):
        if not isinstance(other, Connection):
            return False
        return self.arrival_city == other.arrival_city

    def compare_train_type(self, other):
        if not isinstance(other, Connection):
            return False
        return self.train_type == other.train_type

    def compare_days_of_operation(self, other):
        if not isinstance(other, Connection):
            return False
        
        # If other.days_of_operation is a list (from user selection), use DayParser for exact matching
        if isinstance(other.days_of_operation, list):
            return DayParser.days_match(other.days_of_operation, self.days_of_operation)
        
        # If both are strings, just do simple comparison
        return self.days_of_operation == other.days_of_operation

    def compare_first_class_rate(self, other):
        if not isinstance(other, Connection):
            return False
        return int(self.first_class_rate) == int(other.first_class_rate)

    def compare_second_class_rate(self, other):
        if not isinstance(other, Connection):
            return False
        return int(self.second_class_rate) == int(other.second_class_rate)

    pass
    def __str__(self):
        return (f"Connection(route_id={self.route_id}, departure_city={self.departure_city}, "
                f"arrival_city={self.arrival_city}, departure_time={self.departure_time}, "
                f"arrival_time={self.arrival_time}, train_type={self.train_type}, "
                f"days_of_operation={self.days_of_operation}, first_class_rate={self.first_class_rate}, "
                f"second_class_rate={self.second_class_rate}, trip_time={self.trip_time})")
