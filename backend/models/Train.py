
class Train:
    def __init__(self, train_type):
        self.train_type = train_type

    def __str__(self):
        return self.train_type

    def __eq__(self, other):
        if not isinstance(other, Train):
            return False
        return self.train_type == other.train_type

    pass