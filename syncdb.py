import threading
import multiprocessing
from filedb import Filedb


class Syncdb():
    def __init__(self, database: Filedb, thread_or_process):
        if not isinstance(database, Filedb):
            raise ValueError("not filedb instance")
        self.database = database
        if thread_or_process:
            self.semaphore = threading.Semaphore(10)
            self.lock = threading.Lock()
        else:
            self.semaphore = multiprocessing.Semaphore(10)
            self.lock = multiprocessing.Lock()

    def get_value(self, key):
        self.semaphore.acquire()
        value = self.database.get_value(key)
        self.semaphore.release()
        return value

    def set_value(self, key, val):
        self.lock.acquire()
        for i in range(10):
            self.semaphore.acquire()
        flag = self.database.set_value(key, val)
        self.lock.release()
        for i in range(10):
            self.semaphore.release()
        return flag

    def delete_value(self, key):
        self.lock.acquire()
        for i in range(10):
            self.semaphore.acquire()
        flag = self.database.delete_value(key)
        self.lock.release()
        for i in range(10):
            self.semaphore.release()
        return flag


Syncdb()
