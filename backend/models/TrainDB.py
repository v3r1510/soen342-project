from Train import Train
trains = []

class trainDB:
    def add_train(self, train_type):
        temp_train = Train(train_type)
        if self.search_train(temp_train):
            print("Train type already exists")
            return False
        else:
            trains.append(temp_train)
            return True

    def search_train(self, train):
        if not isinstance(train, Train):
            train = Train(train)

        return train in trains

    def find_train(self, Train):
        if not isinstance(train, Train):
            train = Train(train)

        if train in cities:
            return train
        else:
            return None

    pass