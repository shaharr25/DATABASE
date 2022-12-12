from database import Database
import pickle


class Filedb(Database):
    def __init__(self):
        """
        initializer
        """
        super().__init__()
        with open("dbfile.txt", "wb"):
            pass

    def dump(self):
        """
        writes the dictionary in the file
        :return: None
        """
        with open("dbfile.txt", "wb") as file:
            pickle.dump(self.dict, file)
        # pickling the dict and writing it in a file

    def load(self):
        """
        gets the file into the dictionary
        :return: None
        """
        with open("dbfile.txt", "rb") as file:
            try:
                self.dict = pickle.load(file)
            except:
                print("error")

    def set_value(self, key, val):
        """
        sets a new value in the dictionary file
        :param: key the key of the dictionary
        :param: val value to put in the dictionary
        :return: True if the value added to dictionary and false if not
        """
        self.load()
        flag = super().set_value(key, val)
        self.dump()
        return flag

    def get_value(self, key):
        """
        returns the value from the dictionary file
        :param: key the key of the dictionary
        :return: the value of the key
        """
        self.load()
        return super().get_value(key)

    def delete_value(self, key):
        """
        deletes the value of the key from the dictionary file
        :param key: the key of the dictionary
        :return: the value that was deleted
        """
        self.load()
        val = super().delete_value(key)
        self.dump()
        return val
