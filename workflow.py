import os
import time
import shutil
import bookmeta
from util.util import md5_for_file, open_file
from util.wisefile import walk
from util.wise_log import operate_log, debug_log

dlog = debug_log()
op_log = operate_log()


bookmeta.install_repo('test_repo/metainfo')
bookfile_path = 'test_repo/bookfile'
if not os.path.exists(bookfile_path):
    os.makedirs(bookfile_path)


def _build_additional(src_file):
    return {'sizeInBytes': os.path.getsize(src_file),
            'create_time': time.time(),
            }


def add_file(src_file):
    # check file existance
    if not os.path.isfile(src_file):
        op_log.error('file %s not exists' % src_file)
        return added
    file_id = md5_for_file(src_file)
    rawname, ext = os.path.splitext(os.path.basename(src_file))

    # cp src_file dst_file
    dst_file = os.path.join(bookfile_path, '%s%s' % (file_id, ext))
    if not os.path.isfile(dst_file):
        try:
            shutil.copy(src_file, dst_file)
        except Exception as e:
            op_log.error('failed to copy %s. %s' % (src_file, e))
        else:
            op_log.debug('cp %s' % src_file)

    added = 0
    if bookmeta.exists(file_id):
        # file exists, add rawname only
        bookmeta.load(file_id).add_rawname(rawname)
    else:
        # create meta info and autosave
        additional = _build_additional(src_file)
        bookmeta.BookMeta(file_id, ext, rawname, None, **additional)
        added = 1
    return added


def add_path(root, ext, ignore):
    return walk(root, add_file, ext, ignore)


def get_all():
    return bookmeta.get_all()


def open(obj):
    dst_file = os.path.join(
        bookfile_path,
        '%s%s' % (obj.file_id, obj.file_ext)
    )
    try:
        open_file(dst_file)  # what if file deleted
    except Exception as e:
        dlog.error('open file %s error. %s' % (dst_file, e))


def delete(objs):
    if isinstance(objs, bookmeta.BookMeta):
        objs = [objs]
    for obj in objs:
        op_log.info('del %s' % obj.file_id)
        bookfile = os.path.join(
            bookfile_path,
            '%s%s' % (obj.file_id, obj.file_ext)
        )
        metafile = bookmeta.get_metafile(obj.file_id)

        for tarfile in [bookfile, metafile]:
            if os.path.isfile(tarfile):
                op_log.debug('rm %s' % tarfile)
                os.remove(tarfile)


if __name__ == '__main__':
    add_path('.', '.py', '.git')
    for obj in get_all():
        delete(obj)
    open(obj)
