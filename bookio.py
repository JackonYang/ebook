# -*- coding: utf-8-*-
"""load books to repo


"""
import os
import time
import shutil
from util import md5_for_file, is_hiden

import model
from settings import media_path, ignore_seq


def init_media(path):
    if not os.path.exists(path):
        os.makedirs(path)


db = model.connect()
init_media(media_path)


def add_path(src_path, ext_pool='.pdf', ignore_hidden=True):
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
        if not ext or ext not in ext_pool:  # file extension check
            return 0
        file_meta = {'rawname': [rawname],
                     'ext': ext
                     }
        _add_file(src_path, file_meta)
        return 1
    else:  # dir
        added = 0
        tar_path = set(os.listdir(src_path)) - ignore_seq  # ignore log/.git etc
        for rel_path in tar_path:
            abs_path = os.path.join(src_path, rel_path)
            if not ignore_hidden or not is_hiden(abs_path):  # ignore hidden
                added += add_path(abs_path, ext_pool) or 0
        return added

def _add_file(src_path, file_meta):
    if 'md5' not in file_meta:
        file_meta['md5'] = md5_for_file(src_path)
    if "rawname" in file_meta:
        rawname = file_meta.pop("rawname").pop()
        print "add %s" % rawname
    file_meta.update({
        'sizeInBytes': os.path.getsize(src_path),
        'create_time': time.time()
        })
    db.book.update({'md5': file_meta['md5']}, {"$set": file_meta, "$addToSet": {"rawname": rawname}}, True)

    dst_file = os.path.join(media_path, '%s%s' % (file_meta['md5'], file_meta['ext']))
    if not os.path.exists(dst_file):
        shutil.copy(src_path, dst_file)


if __name__ == "__main__":
    print add_path(u'/media/document/booklist/f_media')
