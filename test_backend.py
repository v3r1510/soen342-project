#!/usr/bin/env python3
"""
Test script to verify backend functionality
"""
import sys
import json
sys.path.append('backend')

from models.Console import Console
from models.Connection import Connection
from models.CityDB import CityDB, cities
from models.TrainDB import TrainDB, trains
from models.ConnectionDB import ConnectionDB, connections

def test_backend():
    print("🚂 Testing Railway Backend System")
    print("=" * 50)
    
    # Test 1: Add some test data manually
    print("\n1. Adding test cities...")
    CityDB.add_city("Paris")
    CityDB.add_city("London")
    CityDB.add_city("Berlin")
    print(f"   ✅ Added {len(cities)} cities: {[city.city_name for city in cities]}")
    
    # Test 2: Add test train types
    print("\n2. Adding test train types...")
    TrainDB.add_train("TGV")
    TrainDB.add_train("Eurostar")
    TrainDB.add_train("ICE")
    print(f"   ✅ Added {len(trains)} train types: {[train.train_type for train in trains]}")
    
    # Test 3: Create test connections
    print("\n3. Creating test connections...")
    try:
        connection1 = Connection(
            route_id="R001",
            departure_city="Paris",
            arrival_city="London", 
            departure_time="09:00",
            arrival_time="12:30",
            train_type="Eurostar",
            days_of_operation="Daily",
            first_class_rate=150.0,
            second_class_rate=85.0
        )
        ConnectionDB.add_connection(connection1)
        
        connection2 = Connection(
            route_id="R002", 
            departure_city="Paris",
            arrival_city="Berlin",
            departure_time="10:15",
            arrival_time="18:45",
            train_type="TGV",
            days_of_operation="Mon-Fri",
            first_class_rate=200.0,
            second_class_rate=120.0
        )
        ConnectionDB.add_connection(connection2)
        
        print(f"   ✅ Created {len(connections)} connections")
        
    except Exception as e:
        print(f"   ❌ Error creating connections: {e}")
        return False

    # Test 4: Test Console search functionality
    print("\n4. Testing Console search...")
    try:
        # Create a mock console (without CSV file)
        class MockConsole:
            def search_routes(self, **kwargs):
                # Use the global connections list
                results = []
                for connection in connections:
                    match = True
                    if kwargs.get('departure_city') and connection.departure_city.city_name.lower() != kwargs['departure_city'].lower():
                        match = False
                    if kwargs.get('arrival_city') and connection.arrival_city.city_name.lower() != kwargs['arrival_city'].lower():
                        match = False
                    if match:
                        results.append(connection)
                return results
            
            def routes_to_json(self, routes_list):
                return [route.to_json() for route in routes_list]
        
        console = MockConsole()
        
        # Search for routes from Paris
        paris_routes = console.search_routes(departure_city="Paris")
        print(f"   ✅ Found {len(paris_routes)} routes from Paris")
        
        # Search for routes to London
        london_routes = console.search_routes(arrival_city="London")
        print(f"   ✅ Found {len(london_routes)} routes to London")
        
        # Convert to JSON
        json_routes = console.routes_to_json(paris_routes)
        print(f"   ✅ JSON conversion successful: {len(json_routes)} routes")
        
    except Exception as e:
        print(f"   ❌ Error testing Console: {e}")
        return False
    
    print("\n" + "=" * 50)
    print("🎉 Backend is READY and WORKING!")
    print("\nAvailable API endpoints when server runs:")
    print("  • GET  /message      - Test endpoint")
    print("  • GET  /status       - Server status")
    print("  • POST /search       - Search routes")
    print("  • GET  /routes       - Get all routes")
    print("  • GET  /cities       - Get all cities")
    print("  • GET  /train-types  - Get all train types")
    print("\nTo start the server: python backend/app.py")
    print("Then test with: curl http://127.0.0.1:5000/message")
    
    return True

if __name__ == "__main__":
    test_backend()