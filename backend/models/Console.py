import pandas as pd
from datetime import datetime, timedelta
from .Connection import Connection
from .ConnectionDB import ConnectionDB
from .CityDB import CityDB
from .TrainDB import TrainDB
from .ClientDB import ClientDB
from .TripDB import TripDB
from .Trip import Trip
from .ReservationDB import ReservationDB

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

        cities_count = len(CityDB.get_all_cities())
        trains_count = len(TrainDB.get_all_trains())
        print(f"Loaded {cities_count} cities and {trains_count} trains")

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

        connections_count = len(ConnectionDB.get_all_connections())
        print(f"Loaded {connections_count} connections")

    def _parse_time(self, time_str):
        
        if not time_str:
            return None
            
        # Handle next day notation
        next_day = False
        if "(+1d)" in time_str:
            next_day = True
            time_str = time_str.replace("(+1d)", "").strip()
        
        # Try different time formats
        formats = ["%H:%M:%S", "%H:%M", "%I:%M:%S %p", "%I:%M %p"]
        for fmt in formats:
            try:
                dt = datetime.strptime(time_str, fmt)
                if next_day:
                    dt += timedelta(days=1)
                return dt
            except ValueError:
                continue
        return None
    
    def _calculate_layover_minutes(self, first_segment, second_segment):
        
        arrival_time = self._parse_time(first_segment.arrival_time)
        departure_time = self._parse_time(second_segment.departure_time)
        
        if not arrival_time or not departure_time:
            return None
        
        # Calculate difference
        layover = departure_time - arrival_time
        return int(layover.total_seconds() / 60)
    
    def _is_daytime(self, time_str):
        
        dt = self._parse_time(time_str)
        if not dt:
            return True  # Default to daytime if can't parse
        
        hour = dt.hour
        return 6 <= hour < 22
    
    def _is_valid_layover(self, first_segment, second_segment):
        
        layover_minutes = self._calculate_layover_minutes(first_segment, second_segment)
        
        if layover_minutes is None:
            return True  # Can't calculate, allow it
        
        # Negative layover means impossible connection
        if layover_minutes < 0:
            return False
        
        # Check if arrival time is during daytime or after hours
        is_daytime = self._is_daytime(first_segment.arrival_time)
        
        if is_daytime:
            # Daytime policy: 30 min to 2 hours
            return 30 <= layover_minutes <= 120
        else:
            # After hours policy: maximum 30 minutes
            return layover_minutes <= 30

    def search_routes(self, departure_city=None, arrival_city=None, departure_time=None, 
                     arrival_time=None, train_type=None, days_of_operation=None, 
                     first_class_rate=None, second_class_rate=None):
       # Search for routes based on criteria, including direct and indirect connections
        
        # If both departure and arrival cities are specified, find multi-hop routes
        if departure_city and arrival_city:
            return self.find_routes_with_connections(
                departure_city, arrival_city, departure_time, arrival_time,
                train_type, days_of_operation, first_class_rate, second_class_rate
            )
        
        # Otherwise, use the original filtering logic
        results = []
        user = Connection("U001", departure_city, arrival_city, departure_time, arrival_time,train_type, days_of_operation, first_class_rate, second_class_rate)
        if departure_city:
            results.append(ConnectionDB.find_departure_city(user))
        if arrival_city:
            results.append(ConnectionDB.find_arrival_city(user))
        if departure_time:
            results.append(ConnectionDB.find_departure_time(user))
        if arrival_time:
            results.append(ConnectionDB.find_arrival_time(user))
        if train_type:
            results.append(ConnectionDB.find_train_type(user))
        if days_of_operation:
            results.append(ConnectionDB.find_days_of_operation(user))
        if first_class_rate:
            results.append(ConnectionDB.find_first_class_rate(user))
        if second_class_rate:
            results.append(ConnectionDB.find_second_class_rate(user))

        if not results:
            return []

        return list(set.intersection(*(set(rlts) for rlts in results)))

    def find_routes_with_connections(self, departure_city, arrival_city, departure_time=None,
                                    arrival_time=None, train_type=None, days_of_operation=None,
                                    first_class_rate=None, second_class_rate=None, max_stops=2):
      
        all_routes = []
        
        # Find direct routes 
        direct_routes = self._find_direct_routes(
            departure_city, arrival_city, departure_time, arrival_time,
            train_type, days_of_operation, first_class_rate, second_class_rate
        )
        all_routes.extend(direct_routes)
        
        # Find 1-stop routes 
        if max_stops >= 1:
            one_stop_routes = self._find_one_stop_routes(
                departure_city, arrival_city, departure_time, arrival_time,
                train_type, days_of_operation, first_class_rate, second_class_rate
            )
            all_routes.extend(one_stop_routes)
        
        # Find 2-stop routes 
        if max_stops >= 2:
            two_stop_routes = self._find_two_stop_routes(
                departure_city, arrival_city, departure_time, arrival_time,
                train_type, days_of_operation, first_class_rate, second_class_rate
            )
            all_routes.extend(two_stop_routes)
        
        # Flatten the grouped routes back to individual segments for backward compatibility
        flattened_results = []
        for route in all_routes:
            for segment in route['segments']:
                flattened_results.append(segment)
        
        return flattened_results
    
    def _find_direct_routes(self, departure_city, arrival_city, departure_time=None,
                           arrival_time=None, train_type=None, days_of_operation=None,
                           first_class_rate=None, second_class_rate=None):
        
        results = []
        user = Connection("U001", departure_city, arrival_city, departure_time, arrival_time,
                         train_type, days_of_operation, first_class_rate, second_class_rate)
        
        results.append(ConnectionDB.find_departure_city(user))
        results.append(ConnectionDB.find_arrival_city(user))
        
        if departure_time:
            results.append(ConnectionDB.find_departure_time(user))
        if arrival_time:
            results.append(ConnectionDB.find_arrival_time(user))
        if train_type:
            results.append(ConnectionDB.find_train_type(user))
        if days_of_operation:
            results.append(ConnectionDB.find_days_of_operation(user))
        if first_class_rate:
            results.append(ConnectionDB.find_first_class_rate(user))
        if second_class_rate:
            results.append(ConnectionDB.find_second_class_rate(user))
        
        if not results:
            return []
        
        direct_connections = list(set.intersection(*(set(rlts) for rlts in results)))
        
        # Wrap direct routes in the same format as multi-hop routes
        return [{
            'route_type': 'direct',
            'segments': [connection]
        } for connection in direct_connections]
    
    def _find_one_stop_routes(self, departure_city, arrival_city, departure_time=None,
                              arrival_time=None, train_type=None, days_of_operation=None,
                              first_class_rate=None, second_class_rate=None):
        
        one_stop_routes = []
        
        # Find all connections leaving from departure_city
        first_segment_user = Connection("U001", departure_city, None, departure_time, None,
                                    train_type, days_of_operation, first_class_rate, second_class_rate)
        first_segments = ConnectionDB.find_departure_city(first_segment_user)
        
        # Apply filters to first segment
        if train_type:
            first_segments = [segment for segment in first_segments if segment.compare_train_type(first_segment_user)]
        if days_of_operation:
            first_segments = [segment for segment in first_segments if segment.compare_days_of_operation(first_segment_user)]
        if first_class_rate:
            first_segments = [segment for segment in first_segments if segment.compare_first_class_rate(first_segment_user)]
        if second_class_rate:
            first_segments = [segment for segment in first_segments if segment.compare_second_class_rate(first_segment_user)]
        
        # For each intermediate city, find connections to final destination
        for first_segment in first_segments:
            intermediate_city = first_segment.arrival_city
            
            # Skip if intermediate is the destination
            if str(intermediate_city) == arrival_city:
                continue
            
            # Find second segment from intermediate to arrival
            second_segment_user = Connection("U002", str(intermediate_city), arrival_city, None, arrival_time,
                                        train_type, days_of_operation, first_class_rate, second_class_rate)
            second_segments = ConnectionDB.find_departure_city(second_segment_user)
            second_segments = [segment for segment in second_segments if segment.compare_arrival_city(second_segment_user)]
            
            # Apply filters to second segment
            if train_type:
                second_segments = [segment for segment in second_segments if segment.compare_train_type(second_segment_user)]
            if days_of_operation:
                second_segments = [segment for segment in second_segments if segment.compare_days_of_operation(second_segment_user)]
            if first_class_rate:
                second_segments = [segment for segment in second_segments if segment.compare_first_class_rate(second_segment_user)]
            if second_class_rate:
                second_segments = [segment for segment in second_segments if segment.compare_second_class_rate(second_segment_user)]
            
            # Add each valid route combination as a grouped journey
            for second_segment in second_segments:
                # Validate layover duration before adding
                if self._is_valid_layover(first_segment, second_segment):
                    one_stop_routes.append({
                        'route_type': '1-stop',
                        'segments': [first_segment, second_segment]
                    })
        
        return one_stop_routes
    
    def _find_two_stop_routes(self, departure_city, arrival_city, departure_time=None,
                              arrival_time=None, train_type=None, days_of_operation=None,
                              first_class_rate=None, second_class_rate=None):
        
        two_stop_routes = []
        
        # Find all connections leaving from departure_city
        first_segment_user = Connection("U001", departure_city, None, departure_time, None,
                                    train_type, days_of_operation, first_class_rate, second_class_rate)
        first_segments = ConnectionDB.find_departure_city(first_segment_user)
        
        # Apply filters to first segment
        if train_type:
            first_segments = [segment for segment in first_segments if segment.compare_train_type(first_segment_user)]
        if days_of_operation:
            first_segments = [segment for segment in first_segments if segment.compare_days_of_operation(first_segment_user)]
        if first_class_rate:
            first_segments = [segment for segment in first_segments if segment.compare_first_class_rate(first_segment_user)]
        if second_class_rate:
            first_segments = [segment for segment in first_segments if segment.compare_second_class_rate(first_segment_user)]
        
        # For each first intermediate city
        for first_segment in first_segments:
            intermediate_city_1 = str(first_segment.arrival_city)
            
            if intermediate_city_1 == arrival_city:
                continue
            
            # Find second segment from intermediate 1
            second_segment_user = Connection("U002", intermediate_city_1, None, None, None,
                                        train_type, days_of_operation, first_class_rate, second_class_rate)
            second_segments = ConnectionDB.find_departure_city(second_segment_user)
            
            # Apply filters
            if train_type:
                second_segments = [segment for segment in second_segments if segment.compare_train_type(second_segment_user)]
            if days_of_operation:
                second_segments = [segment for segment in second_segments if segment.compare_days_of_operation(second_segment_user)]
            if first_class_rate:
                second_segments = [segment for segment in second_segments if segment.compare_first_class_rate(second_segment_user)]
            if second_class_rate:
                second_segments = [segment for segment in second_segments if segment.compare_second_class_rate(second_segment_user)]
            
            # For each second intermediate city
            for second_segment in second_segments:
                intermediate_city_2 = str(second_segment.arrival_city)
                
                if intermediate_city_2 == arrival_city or intermediate_city_2 == departure_city:
                    continue
                
                # Find final segment to destination
                final_segment_user = Connection("U003", intermediate_city_2, arrival_city, None, arrival_time,
                                           train_type, days_of_operation, first_class_rate, second_class_rate)
                final_segments = ConnectionDB.find_departure_city(final_segment_user)
                final_segments = [segment for segment in final_segments if segment.compare_arrival_city(final_segment_user)]
                
                # Apply filters
                if train_type:
                    final_segments = [segment for segment in final_segments if segment.compare_train_type(final_segment_user)]
                if days_of_operation:
                    final_segments = [segment for segment in final_segments if segment.compare_days_of_operation(final_segment_user)]
                if first_class_rate:
                    final_segments = [segment for segment in final_segments if segment.compare_first_class_rate(final_segment_user)]
                if second_class_rate:
                    final_segments = [segment for segment in final_segments if segment.compare_second_class_rate(final_segment_user)]
                
                # Add each valid route combination as a grouped journey
                for final_segment in final_segments:
                    # Validate both layovers before adding
                    if (self._is_valid_layover(first_segment, second_segment) and 
                        self._is_valid_layover(second_segment, final_segment)):
                        two_stop_routes.append({
                            'route_type': '2-stop',
                            'segments': [first_segment, second_segment, final_segment]
                        })
        
        return two_stop_routes

    def get_all_routes(self):
        """Get all available routes"""
        return ConnectionDB.get_all_connections()

    def get_all_cities(self):
        """Get all available cities"""
        cities = CityDB.get_all_cities()
        return [city.city_name for city in cities]

    def get_all_train_types(self):
        """Get all available train types"""
        trains = TrainDB.get_all_trains()
        return [train.train_type for train in trains]

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
                reservation = trip.add_reservation(client)
            except ValueError as e:
                # Client already has a reservation for this connection
                raise ValueError(f"Error booking trip: {str(e)}")

            ReservationDB.add_reservation(trip, reservation)

        # Save trip to database
        TripDB.add_trip(trip)
        
        return trip

    def get_all_clients(self):
        """Get all clients who have made reservations"""
        return ClientDB.get_all_clients()

    def get_all_trips(self):
        """Get all booked trips"""
        return TripDB.get_all_trips()

    def find_trip_by_id(self, trip_id):
        """Find a specific trip by ID"""
        return TripDB.find_trip(trip_id)

    def find_client_trips(self, client_id):
        """Find all trips for a specific client"""
        client = ClientDB.find_client(client_id)
        if not client:
            return []
        return TripDB.find_trips_by_client(client)
