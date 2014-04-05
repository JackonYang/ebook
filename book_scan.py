# -*- coding: utf-8-*-
"""load books to repo


"""
import os
import time
import shutil
from util import md5_for_file, is_hiden

import model
from settings import media_path, ignore_seq


class BookScan():

    def __init__(self, src_path, output, ext_pool='.pdf', ignore_hidden=True):
        self.db = model.connect()
        if not os.path.exists(media_path):
            os.makedirs(media_path)
        self.ext_pool = ext_pool
        self.ignore_hidden = ignore_hidden
        self.src_path = src_path
        self.output = output
        self.flag = True

    def start(self):
        self.output('%s books added\n' % self.add_path(self.src_path))

    def add_path(self, src_path):
        """add file/dir and copy files.

        @src_path: unicode encoding is required
        @ext_pool: startswith . and separated by ,
        @ignore_hidden: boolen

        """
        if not os.path.exists(src_path):  # not exists
            return None

        # common check
        # sensitive information

        if os.path.isfile(src_path):  # file
            rawname, ext = os.path.splitext(os.path.basename(src_path))
            if not ext or ext not in self.ext_pool:  # file extension check
                return 0
            file_meta = {'rawname': [rawname],
                         'ext': ext
                         }
            self._add_file(src_path, file_meta)
            return 1
        else:  # dir
            added = 0
            # ignore log/.git etc
            tar_path = set(os.listdir(src_path)) - ignore_seq
            for rel_path in tar_path:
                abs_path = os.path.join(src_path, rel_path)
                if not self.ignore_hidden or not is_hiden(abs_path):
                    # ignore hidden
                    added += self.add_path(abs_path) or 0
            return added

    def StopScan(self):
        self.flag = False

    def _add_file(self, src_path, file_meta):
        if 'md5' not in file_meta:
            file_meta['md5'] = md5_for_file(src_path)
        if "rawname" in file_meta:
            rawname = file_meta.pop("rawname").pop()
            self.output("add %s\n" % rawname)
        file_meta.update({'sizeInBytes': os.path.getsize(src_path),
                          'create_time': time.time()
                          })
        matcher = {'md5': file_meta['md5']}
        setter = {"$set": file_meta, "$addToSet": {"rawname": rawname}}
        self.db.book.update(matcher, setter, True)

        filename = '%s%s' % (file_meta['md5'], file_meta['ext'])
        dst_file = os.path.join(media_path, filename)
        if not os.path.exists(dst_file):
            shutil.copy(src_path, dst_file)


if __name__ == "__main__":
    import sys
    scanner = BookScan(u'/media/document/books', sys.stdout.write)
    # daemonic 为 True 时，表示主线程结束时子线程也要跟着退出
    #scanner.setDaemon(True)
    scanner.start()
