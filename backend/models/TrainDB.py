from .Train import Train
from .Database import Database

class TrainDB:
    @staticmethod
    def add_train(train_type):
        
        if TrainDB.search_train(train_type):
            print("Train type already exists")
            return False
        
        query = "INSERT INTO Trains (train_type) VALUES (?)"
        result = Database.execute_query(query, (train_type,))
        return result is not None
    
    @staticmethod
    def search_train(train):

        if isinstance(train, Train):
            train_type = train.train_type
        else:
            train_type = train
        
        query = "SELECT train_id, train_type FROM Trains WHERE train_type = ?"
        result = Database.execute_query(query, (train_type,), fetch_one=True)
        return result is not None
    
    @staticmethod
    def find_train(train_name):
 
        if isinstance(train_name, Train):
            train_type = train_name.train_type
        else:
            train_type = train_name
        
        query = "SELECT train_id, train_type FROM Trains WHERE train_type = ?"
        result = Database.execute_query(query, (train_type,), fetch_one=True)
        
        if result:
            return Train(result[1])
        return None
    
    @staticmethod
    def get_all_trains():

        query = "SELECT train_id, train_type FROM Trains"
        results = Database.execute_query(query, fetch_all=True)
        
        if results:
            return [Train(row[1]) for row in results]
        return []
