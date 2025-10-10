class City:
    def __init__(self, city_name):
        self.city_name = city_name

    def __str__(self):
        return self.city_name

    def __eq__(self, other):
        if not isinstance(other, City):
            return False
        return self.city_name == other.city_name


    pass