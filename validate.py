import os
import sys
import re
from cfg import get_cfg
import settings
import codecs
import fnmatch
from util.util import is_hiden

tar_file = os.path.join(settings.op_log_path, 'info.log')

para_cfg = get_cfg()

ptn = re.compile(r'\|INFO\|del\s+(.+?\.pdf)')
def get_dels():
    if os.path.isfile(tar_file):
        with open(tar_file, 'r') as f:
            content = f.read()
        return ptn.findall(content)
    return []


def get_ignore():
    return para_cfg['ignore']


def utf8_required(func):
    def wrap(path, *args, **kwargs):
        if isinstance(path, str):
            path = path.decode(sys.getfilesystemencoding())
        return func(path, *args, **kwargs)
    return wrap


_deleted = get_dels()
def is_deleted(file_id):
    return file_id in _deleted

@utf8_required
def is_ignore(path, ignore_hiden=True):
    # ignore_hiden
    if ignore_hiden and is_hiden(path):
        return True

    # ignore _ignore_seq
    for ptn in get_ignore():
        if fnmatch.fnmatch(path, ptn):
            return True
    return False

def validate_ext(filename, ext_range):
    ext_range = ext_range.strip(',')
    if ',' in ext_range:
        ext_seq = ext_range.split(',')
    else:
        ext_seq = [ext_range]
    prefix, ext = os.path.splitext(filename)
    if ext and ext.strip('.') in [item.strip('*. ') for item in ext_seq]:
        return True
    return False

if __name__ == '__main__':
    print get_ignore()
    print is_deleted('adfadf')
    print is_deleted('7e1a8aac1699e1ffc0a4eadbcc5dc07e.pdf')
