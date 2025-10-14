from .Train import Train
trains = []

class TrainDB:
    @staticmethod
    def add_train(train_type):
        temp_train = Train(train_type)
        if TrainDB.search_train(temp_train):
            print("Train type already exists")
            return False
        else:
            trains.append(temp_train)
            return True
    @staticmethod
    def search_train(train):
        if not isinstance(train, Train):
            train = Train(train)

        return train in trains
    @staticmethod
    def find_train(train_name):
        if not isinstance(train_name, Train):
            train = Train(train_name)
        else:
            train = train_name

        for t in trains:
            if t == train:
                return t
        return None