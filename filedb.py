from database import Database
import pickle


class Filedb(Database):
    def __init__(self):
        """
        initializer
        """
        super().__init__()

    def dump(self):
        with open("dbfile.txt", "wb") as file:
            pickle.dump(self.dict, file)
        # pickling the dict and writing it in a file

    def load(self):
        with open("dbfile.txt", "rb") as file:
            self.dict = pickle.load(file)

    def set_value(self, key, val):
        """
        override
        """
        self.load()
        flag = super().set_value(key, val)
        self.dump()
        return flag

    def get_value(self, key):
        self.load()
        return super().get_value(key)

    def delete_value(self,key):
        self.load()
        val = super().delete_value(key)
        self.dump()
        return val


db = Filedb()
db.dump()
