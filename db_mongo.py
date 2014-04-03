# -*- coding: utf-8-*-
import pymongo
from settings import db_ip, db_port, db_name


def connect(ip=db_ip, port=db_port, name=db_name):
    conn = pymongo.Connection(ip, port)
    return conn[name]


if __name__ == "__main__":
    print connect()
