from flask import Flask, request, jsonify, Blueprint
from models.Console import Console

bp = Blueprint('controller', __name__, url_prefix='/')


console = None

def initialize_console(filename):
    global console
    console = Console(filename)

@bp.route('/search', methods=['POST'])
def search_routes():
    """Search for routes based on criteria from frontend"""
    if not console:
        return jsonify({"error": "System not initialized"}), 500
    
    try:
        data = request.get_json()
        
    
        departure_city = data.get('departureCity', '').strip()
        arrival_city = data.get('arrivalCity', '').strip()
        departure_time = data.get('departureTime', '').strip()
        arrival_time = data.get('arrivalTime', '').strip()
        train_type = data.get('trainType', '').strip()
        days_of_operation = data.get('operationDays', '').strip()
        first_class_rate = data.get('firstRate')
        second_class_rate = data.get('secondRate')
        
  
        departure_city = departure_city if departure_city else None
        arrival_city = arrival_city if arrival_city else None
        departure_time = departure_time if departure_time else None
        arrival_time = arrival_time if arrival_time else None
        train_type = train_type if train_type else None
        days_of_operation = days_of_operation if days_of_operation else None
        
 
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
        
        routes_json = console.routes_to_json(results)
        
        return jsonify({
            "success": True,
            "routes": routes_json,
            "count": len(routes_json)
        })
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@bp.route('/routes', methods=['GET'])
def get_all_routes():
    """Get all available routes"""
    if not console:
        return jsonify({"error": "System not initialized"}), 500
    
    try:
        routes = console.get_all_routes()
        routes_json = console.routes_to_json(routes)
        
        return jsonify({
            "success": True,
            "routes": routes_json,
            "count": len(routes_json)
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@bp.route('/cities', methods=['GET'])
def get_cities():
    """Get all available cities"""
    if not console:
        return jsonify({"error": "System not initialized"}), 500
    
    try:
        cities = console.get_all_cities()
        return jsonify({
            "success": True,
            "cities": cities
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@bp.route('/train-types', methods=['GET'])
def get_train_types():
    """Get all available train types"""
    if not console:
        return jsonify({"error": "System not initialized"}), 500
    
    try:
        train_types = console.get_all_train_types()
        return jsonify({
            "success": True,
            "train_types": train_types
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@bp.route('/book-trip', methods=['POST'])
def book_trip():
    """
    Book a trip for one or more travelers
    
    Expected JSON format:
    {
        "route_id": "R001",
        "travelers": [
            {"name": "John Doe", "age": 35, "client_id": "ID123456"},
            {"name": "Jane Doe", "age": 33, "client_id": "ID789012"}
        ]
    }
    """
    if not console:
        return jsonify({"error": "System not initialized"}), 500
    
    try:
        data = request.get_json()
        

        if 'route_id' not in data or 'travelers' not in data:
            return jsonify({"error": "Missing required fields: route_id and travelers"}), 400
        
        route_id = data['route_id']
        travelers = data['travelers']
        
 
        if not isinstance(travelers, list) or len(travelers) == 0:
            return jsonify({"error": "At least one traveler is required"}), 400
        
        for traveler in travelers:
            if 'name' not in traveler or 'age' not in traveler or 'client_id' not in traveler:
                return jsonify({"error": "Each traveler must have name, age, and client_id"}), 400
        
  
        from models.ConnectionDB import connections
        connection = None
        for conn in connections:
            if conn.route_id == route_id:
                connection = conn
                break
        
        if not connection:
            return jsonify({"error": f"Connection with route_id {route_id} not found"}), 404
        
  
        trip = console.book_trip(travelers, connection)
        
        return jsonify({
            "success": True,
            "message": "Trip booked successfully",
            "trip": trip.to_json()
        })
        
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@bp.route('/trips', methods=['GET'])
def get_all_trips():
    """Get all booked trips"""
    if not console:
        return jsonify({"error": "System not initialized"}), 500
    
    try:
        trips = console.get_all_trips()
        return jsonify({
            "success": True,
            "trips": [trip.to_json() for trip in trips],
            "count": len(trips)
        })
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
        trips = console.find_client_trips(client_id)
        return jsonify({
            "success": True,
            "trips": [trip.to_json() for trip in trips],
            "count": len(trips)
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

#this will be the link between the back and the front end, get posts html request etc, now i sleep 
