class City:
    __slots__ = ("city_name",)

    def __init__(self, city_name):
        self.city_name = city_name

    def __str__(self):
        return self.city_name

    def __eq__(self, other):
        if not isinstance(other, City):
            return NotImplemented
        return self.city_name == other.city_name

    def __hash__(self):
        return hash(self.city_name)
    
    def to_json(self):
        return {
            "name": self.name,
        }
    pass
