import threading
import multiprocessing
from filedb import Filedb
import logging


class Syncdb():
    def __init__(self, database: Filedb, thread_or_process):
        """
        initializer
        :param database: dictionary
        :param thread_or_process: true if thread and false if proces
        """
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
        """
        let only 10 readers read at the same time
        :param: key the key of the dictionary
        :return: the value of the key
        """
        self.semaphore.acquire()
        logging.debug("reader in")
        value = self.database.get_value(key)
        self.semaphore.release()
        logging.debug("reader out")
        return value

    def set_value(self, key, val):
        """
        let only one user set a new value in the dictionary with no other readers or writers at the same time
        :param: key the key of the dictionary
        :param: val value to put in the dictionary
        :return: True if the value added to dictionary and false if not
        """
        self.lock.acquire()
        for i in range(10):
            self.semaphore.acquire()
        logging.debug("writer in")
        flag = self.database.set_value(key, val)
        for i in range(10):
            self.semaphore.release()
        logging.debug("writer out")
        self.lock.release()
        return flag

    def delete_value(self, key):
        """
        let only one user to delete from the dictionary with no other readers or writers at the same time
        :param key: the key of the dictionary
        :return: the value that was deleted
        """
        self.lock.acquire()
        for i in range(10):
            self.semaphore.acquire()
        flag = self.database.delete_value(key)
        for i in range(10):
            self.semaphore.release()
        self.lock.release()
        return flag


