from flask import Flask, request, jsonify, Blueprint
from models.Console import Console
from models.ConnectionDB import ConnectionDB
import json

bp = Blueprint('controller', __name__, url_prefix='/')

console = None

def initialize_console(filename):
    global console  #console object that can be used anywhere in teh code
    console = Console(filename)
initialize_console("eu_rail_network.csv") #file where the connections are loaded from

@bp.route('/search', methods=['POST', 'GET'])
def search_routes():
    """Search for routes based on criteria from frontend"""
    if not console:
        return jsonify({"error": "System not initialized"}), 500
    
    try:
        data = request.get_json()
        # Extract search criteria from frontend
        departure_city = data.get('departureCity', '').strip()
        arrival_city = data.get('arrivalCity', '').strip()
        departure_time = data.get('departureTime', '').strip()
        arrival_time = data.get('arrivalTime', '').strip()
        train_type = data.get('trainType', '').strip()
        
        # Handle days_of_operation as either string or array
        days_of_operation = data.get('operationDays')
        if isinstance(days_of_operation, str):
            days_of_operation = days_of_operation.strip() if days_of_operation else None
        elif isinstance(days_of_operation, list):
            days_of_operation = days_of_operation if len(days_of_operation) > 0 else None
        else:
            days_of_operation = None
        
        first_class_rate = data.get('firstRate')
        second_class_rate = data.get('secondRate')
        
  
        departure_city = departure_city if departure_city else None
        arrival_city = arrival_city if arrival_city else None
        departure_time = departure_time if departure_time else None
        arrival_time = arrival_time if arrival_time else None
        train_type = train_type if train_type else None
        
 
        results = console.search_routes(
            departure_city=departure_city,
            arrival_city=arrival_city,
            departure_time=departure_time,
            arrival_time=arrival_time,
            train_type=train_type,
            days_of_operation=days_of_operation,
            first_class_rate=first_class_rate,
            second_class_rate=second_class_rate
        )
        print(f"Found {len(results)} matching routes")
        # Convert to JSON format
        routes_json = console.routes_to_json(results)
        #sends back the searched routes
        return jsonify({
            "success": True,
            "routes": routes_json,
            "count": len(routes_json)
        }), 200
        
    except Exception as e:
        return jsonify({"error (this is a big error)": str(e)}), 500


@bp.route('/book-trip', methods=['POST'])
def api_book_trip():
    if not console:
        return jsonify({"error": "System not initialized"}), 500

    try:
        data = request.get_json()

        # basic payload validation
        if 'route_id' not in data or 'travelers' not in data:
            return jsonify({"error": "Missing required fields: route_id and travelers"}), 400

        route_id = data['route_id']
        travelers = data['travelers']
        date = data['trip_date']

        if not isinstance(travelers, list) or len(travelers) == 0:
            return jsonify({"error": "At least one traveler is required"}), 400

        # sanitize travel_class for each traveler
        for traveler in travelers:
            if ('name' not in traveler or
                    'age' not in traveler or
                    'client_id' not in traveler or
                    'travel_class' not in traveler):
                return jsonify({
                    "error": "Each traveler must have name, age, client_id, and travel_class"
                }), 400

            # keep just 'first' or 'second' for the travel class
            travel_class = traveler['travel_class'].lower().strip()
            if 'first' in travel_class:
                traveler['travel_class'] = 'first'
            elif 'second' in travel_class:
                traveler['travel_class'] = 'second'
            else:
                return jsonify({
                    "error": "Each traveler must have name, age, travel class and client_id"
                }), 400

        # find the Connection object for this route_id
        all_connections = ConnectionDB.get_all_connections()
        connection = next(
            (c for c in all_connections if str(c.route_id) == str(route_id)),
            None
        )

        if not connection:
            return jsonify({
                "error": f"Connection with route_id {route_id} not found"
            }), 404

        # ask Console to book the trip
        trip = console.book_trip(travelers, connection, date)
        if trip is None:
            return jsonify({
                "error": "Internal error: trip object is None (check console.book_trip / TripDB)"
            }), 500

        #success, returns the fact that the booking has been succesfully done
        return jsonify({
            "success": True,
            "message": "Trip booked successfully",
        }), 200

    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@bp.route('/trip/<trip_id>', methods=['GET'])
def get_trip(trip_id):
    """Get a specific trip by ID"""
    if not console:
        return jsonify({"error": "System not initialized"}), 500
    
    try:
        trip = console.find_trip_by_id(trip_id)
        if not trip:
            return jsonify({"error": "Trip not found"}), 404
        
        return jsonify({
            "success": True,
            "trip": trip.to_json()
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@bp.route('/client/<client_id>/trips', methods=['GET'])
def get_client_trips(client_id):
    """Get all trips for a specific client"""
    if not console:
        return jsonify({"error": "System not initialized"}), 500
    
    try:
        reservations = console.find_client_reservations(client_id)
        #sends back the trips information and reservation information
        return jsonify({
                "success": True,
                "trips": [reservation.to_json() for reservation in reservations],
                "count": len(reservations)
            }), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

#this will be the link between the back and the front end, get posts html request etc, now i sleep 
