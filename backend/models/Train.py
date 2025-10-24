
class Train:
    __slots__ = ("train_type",)

    def __init__(self, train_type):
        self.train_type = train_type

    def __str__(self):
        return self.train_type

    def __eq__(self, other):
        if not isinstance(other, Train):
            return NotImplemented
        return self.train_type == other.train_type

    def __hash__(self):
        return hash(self.train_type)
    def to_json(self):
        return {
            "type": self.train_type,
        }
    pass