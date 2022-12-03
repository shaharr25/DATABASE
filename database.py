class Database():
    def __init__(self):
        """
        initializer
        """
        self.dict = {}

    def set_value(self, key, val):
        """

        :param key:
        :param val:
        :return:
        """
        self.dict[key] = val
        if key in self.dict.keys():
            return True
        else:
            return False

    def get_value(self, key):
        return self.dict.get(key)

    def delete_value(self, key):
        if key in self.dict.keys():
            value = self.get_value(key)
            del self.dict[key]
            return value
        else:
            raise KeyError("key does not exist")


db = Database()
db.set_value("a", "b")
print(db.dict)
print(db.get_value("a"))
print(db.dict)
