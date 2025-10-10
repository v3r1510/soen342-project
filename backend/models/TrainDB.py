from Train import Train
trains = []

class trainDB:
    @staticmethod
    def add_train(self, train_type):
        temp_train = Train(train_type)
        if self.search_train(temp_train):
            print("Train type already exists")
            return False
        else:
            trains.append(temp_train)
            return True
    @staticmethod
    def search_train(self, train):
        if not isinstance(train, Train):
            train = Train(train)

        return train in trains
    @staticmethod
    def find_train(self, Train):
        if not isinstance(train, Train):
            train = Train(train)

        for t in trains:
            if t == train:
                return t
        return None

    pass