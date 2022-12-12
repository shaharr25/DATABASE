from syncdb import Syncdb
from filedb import Filedb
from multiprocessing import Process
import logging


def writer(db, id):
    """
    writer gets access to write to the dictionary
    :param db: dictionary
    :return:  None
    """
    logging.debug("writer " + str(id) + " joined")
    for i in range(100):
        assert db.set_value(i, i)
    for i in range(100):
        flag = db.delete_value(i) == i or db.delete_value(i) is None
        assert flag
    logging.debug("writer " + str(id) + " left")


def reader(db):
    """
    reader gets access to read value from the dictionary
    :param db: dictionary
    :return: None
    """
    logging.debug("reader joined")
    for i in range(100):
        flag = db.get_value(i) is None or db.get_value(i) == i
        assert flag
    logging.debug("reader left")


def main():
    logging.basicConfig(filename='logprocess.txt', level=logging.DEBUG,
                        format='%(asctime)s %(levelname)s %(threadName)s %(message)s')
    db = Syncdb(Filedb(), False)
    for i in range(200, 300):
        db.set_value(i, i)
    logging.debug("no competition")
    writer(db, 0)
    reader(db)
    logging.debug("in competition")
    all_processes = []
    i = 1
    for i in range(0, 10):
        process1 = Process(target=writer, args=(db, i))
        i += 1
        all_processes.append(process1)
        process1.start()
    for i in range(0, 50):
        process1 = Process(target=reader, args=(db, ))
        all_processes.append(process1)
        process1.start()
    for i in all_processes:
        i.join()
    for i in range(200, 300):
        assert db.get_value(i) == i


if __name__ == "__main__":
    main()
