from .City import City
from .Database import Database

class CityDB:
    @staticmethod
    def add_city(city_name):
       
        if CityDB.search_city(city_name):
            print("City already exists")
            return False
        
        query = "INSERT INTO Cities (City_name) VALUES (?)"
        result = Database.execute_query(query, (city_name,))
        return result is not None
    
    @staticmethod
    def search_city(city):
       
        if isinstance(city, City):
            city_name = city.city_name
        else:
            city_name = city
        
        query = "SELECT City_name FROM Cities WHERE City_name = ?"
        result = Database.execute_query(query, (city_name,), fetch_one=True)
        return result is not None
    
    @staticmethod
    def find_city(city):
        
        if isinstance(city, City):
            city_name = city.city_name
        else:
            city_name = city
        
        query = "SELECT City_name FROM Cities WHERE City_name = ?"
        result = Database.execute_query(query, (city_name,), fetch_one=True)
        
        if result:
            return City(result[0])
        return None
    
    @staticmethod
    def get_all_cities():
        query = "SELECT City_name FROM Cities"
        results = Database.execute_query(query, fetch_all=True)
        
        if results:
            return [City(row[0]) for row in results]
        return []