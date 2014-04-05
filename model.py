# -*- coding: utf-8-*-
"""model for book meta info

"""
import sys
import os

import pymongo
from settings import db_ip, db_port, db_name, media_path


def connect(ip=db_ip, port=db_port, name=db_name):
    conn = pymongo.Connection(ip, port)
    return conn[name]

db = connect()


def _clean_str(string):
    """convert utf8 unicode if string is str

    filesystemencoding is used to decode

    """
    if isinstance(string, str):
        string = string.decode(sys.getfilesystemencoding())
    return string


def get_all():
    return [BookMeta(meta_info) for meta_info in db.book.find()]


class BookMeta:
    """Meta info of a single book

    """

    def __init__(self, meta):
        self.meta = meta
        self.md5 = meta['md5']
        self.ext = meta['ext']

    def get_media_path(self):
        return os.path.join(media_path, self.md5 + self.ext)

    def get_dispname(self):
        return self.meta.get('dispname', ','.join(self.meta['rawname']))

    def set_dispname(self, dispname):
        self.meta['dispname'] = dispname
        db.book.update({'md5': self.md5}, {"$set": {"dispname": dispname}})

    def get_sizeInMb(self):
        return self.meta.get('sizeInBytes', 0) / (1024.0*1024.0)

    def get_book_language(self):
        return self.meta.get('language', '')


if __name__ == '__main__':
    pass
