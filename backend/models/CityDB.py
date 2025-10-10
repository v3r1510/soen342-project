from City import City

cities = []

class CityDB:
    def add_city(self, city_name):
        temp_city = City(city_name)
        if self.search_city(temp_city):
            print("City already exists")
            return False
        else:
            cities.append(temp_city)
            return True

    def search_city(self, city):
        if not isinstance(city, City):
            city = City(city)

        return city in cities

    def find_city(self, city):
        if not isinstance(city, City):
            city = City(city)

        if city in cities:
            return city
        else:
            return None

    pass