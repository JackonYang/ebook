import os
import sys
import time
from util.util import md5_for_file
from util.wisefile import walk
from model import BookMeta
import storage
from settings import repo_path


# init repo path
store = storage.build_repo(repo_path)


def _build_additional(src_file):
    return {'sizeInBytes': os.path.getsize(src_file),
            'create_time': time.time(),
            }


def add_file(src_file, file_id=None):
    # check file existance
    if not os.path.isfile(src_file):
        return 0
    if not file_id:
        file_id = md5_for_file(src_file)
    rawname, ext = os.path.splitext(os.path.basename(src_file))

    if store.meta_exists(file_id):
        # file exists, add rawname only. do not copy src_file
        meta_obj = BookMeta.feed(store.load(file_id))
        meta_obj.add_rawname(rawname)
        return store.update_on_exists(file_id, unicode(meta_obj), src_file=None)

    additional = _build_additional(src_file)
    meta_obj = BookMeta(file_id, ext, rawname, None, **additional)
    return store.update_on_exists(file_id, unicode(meta_obj), src_file)


def add_path(root, ext='.pdf', ignore='.git, .*'):
    return walk(root, add_file, ext, ignore)


if __name__ == '__main__':
    if len(sys.argv) > 1:
        for root in sys.argv[1:]:
            print 'begin to add %s' % root
            print '%s files added' % add_path(root, '.pdf', '.git, .*')
    else:
        print 'no root'
