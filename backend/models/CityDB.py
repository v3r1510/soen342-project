from .City import City

cities = []

class CityDB:
    @staticmethod
    def add_city(city_name):
        temp_city = City(city_name)
        if CityDB.search_city(temp_city):
            print("City already exists")
            return False
        else:
            cities.append(temp_city)
            return True
    @staticmethod
    def search_city(city):
        if not isinstance(city, City):
            city = City(city)

        return city in cities
    @staticmethod
    def find_city(city):
        if not isinstance(city, City):
            city = City(city)

        for c in cities:
            if c == city:
                return c
        return None