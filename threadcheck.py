from syncdb import Syncdb
from filedb import Filedb
from threading import Thread
import logging


def writer(db):
    """
    writer gets access to write to the dictionary
    :param db: dictionary
    :return:  None
    """
    logging.debug("writer joined")
    for i in range(100):
        assert db.set_value(i, i)
    for i in range(100):
        flag = db.delete_value(i) == i or db.delete_value(i) is None
        assert flag
    logging.debug("writer left")


def reader(db):
    """
    reader gets access to read value from the dictionary
    :param db: dictionary
    :return: None
    """
    logging.debug("reader joined")
    for i in range(100):
        flag = db.get_value(i) == i or db.get_value(i) is None
        assert flag
    logging.debug("reader left")


def main():
    logging.basicConfig(filename='logthread.txt', level=logging.DEBUG,
                        format='%(asctime)s %(levelname)s %(threadName)s %(message)s')
    db = Syncdb(Filedb(), True)
    logging.debug("no competition")
    writer(db)
    reader(db)
    logging.debug("in competition")
    all_threads = []
    for i in range(0, 10):
        thread = Thread(target=writer, args=(db, ))
        all_threads.append(thread)
        thread.start()
    for i in range(0, 50):
        thread = Thread(target=reader, args=(db, ))
        all_threads.append(thread)
        thread.start()
    for i in all_threads:
        i.join()


if __name__ == "__main__":
    main()
