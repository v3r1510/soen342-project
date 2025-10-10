from flask import Flask, request, jsonify, Blueprint
from models.Console import Console

bp = Blueprint('controller', __name__, url_prefix='/')

# Initialize console with data file (you'll need to add your CSV file)
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
        
        # Extract search criteria from frontend
        departure_city = data.get('departureCity', '').strip()
        arrival_city = data.get('arrivalCity', '').strip()
        departure_time = data.get('departureTime', '').strip()
        arrival_time = data.get('arrivalTime', '').strip()
        train_type = data.get('trainType', '').strip()
        days_of_operation = data.get('operationDays', '').strip()
        first_class_rate = data.get('firstRate')
        second_class_rate = data.get('secondRate')
        
        # Convert empty strings to None
        departure_city = departure_city if departure_city else None
        arrival_city = arrival_city if arrival_city else None
        departure_time = departure_time if departure_time else None
        arrival_time = arrival_time if arrival_time else None
        train_type = train_type if train_type else None
        days_of_operation = days_of_operation if days_of_operation else None
        
        # Search routes
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
        
        # Convert to JSON format
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

#this will be the link between the back and the front end, get posts html request etc, now i sleep 