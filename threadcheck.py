from syncdb import Syncdb
from filedb import Filedb
from threading import Thread
import logging


def writer(db):
    logging.debug("writer joined")
    for i in range(100):
        assert db.set_value(i, i)
    logging.debug("writer left")


def reader(db):
    logging.debug("reader joined")
    for i in range(100):
        assert i == db.get_value(i)
    logging.debug("reader left")


def main():
    logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(levelname)s %(threadName)s %(message)s')
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
    for i in all_threads:
        i.join()
    for i in range(0, 50):
        thread = Thread(target=reader, args=(db, ))
        all_threads.append(thread)
        thread.start()
    for i in all_threads:
        i.join()


if __name__ == "__main__":
    main()


