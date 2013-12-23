import os
import re
import settings

tar_file = os.path.join(settings.op_log_path, 'info.log')

ptn = re.compile(r'\|INFO\|del\s+(.+?\.pdf)')
def get_dels():
    if os.path.isfile(tar_file):
        with open(tar_file, 'r') as f:
            content = f.read()
        return ptn.findall(content)
    return []

def get_ignore():
    return settings.ignore_seq

_deleted = get_dels()
def is_deleted(file_id):
    return file_id in _deleted

_ignore = get_ignore()
def is_ignore(path, ignore_hiden=True):
    # ignore_hiden
    if ignore_hiden and path.startswith('.'):
        return True

    # ignore _ignore_seq
    if path in _ignore:
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
    print is_deleted('adfadf')
    print is_deleted('7e1a8aac1699e1ffc0a4eadbcc5dc07e.pdf')
