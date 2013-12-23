# -*- coding: utf-8-*-
import os
import shutil
from model import FileMeta
from util.util import md5_for_file
from util.util import open_file as open_file_
import settings
from util.wise_log import operate_log, debug_log
if __name__ == '__main__':
    log = debug_log()
    op_log = operate_log()
else:
    log = debug_log()
    op_log = operate_log(settings.op_log_path)

_ignore_seq = settings.ignore_seq

def _is_ignore_path(path, ignore_hiden=True):
    # ignore_hiden
    if ignore_hiden and path.startswith('.'):
        return True

    # ignore _ignore_seq
    if path in _ignore_seq:
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


class FlatFile:

    def __init__(self, repo_path, metafile='meta.json'):
        self.repo_path = repo_path
        _ignore_seq.add(repo_path)
        if not os.path.exists(self.repo_path):
            os.makedirs(self.repo_path)

        FileMeta.init_mng(os.path.join(self.repo_path, metafile))

    def open(self, obj):
        open_file(self._file_path(obj.file_id))

    def add_file(self, src_file, metainfo=None):
        count = 0
        if not os.path.isfile(src_file):
            op_log.error('file %s not exists' % src_file)
            return count

        if metainfo is None:
            metainfo = self._build_meta(src_file)

        dst_file = self._file_path(metainfo.file_id)
        if not os.path.isfile(dst_file):
            # cp src_file dst_file
            try:
                shutil.copy(src_file, dst_file)
            except Exception as e:
                op_log.error('failed to copy %s. %s' % (src_file, e))
            else:
                op_log.debug('cp %s' % src_file)

        if os.path.isfile(dst_file):
            # add meta info
            if FileMeta.mng.add_if_exists(metainfo):
                op_log.info('add %s' % src_file)
                count = 1
        return count

    def add_path(self, src_path, ext='*.pdf'):
        if not os.path.exists(src_path):
            return 0
        elif os.path.isfile(src_path):
            return self.add_file(src_path)
        added = 0
        for rel_path in os.listdir(src_path):
            abs_path = os.path.join(src_path, rel_path)
            if _is_ignore_path(rel_path):
                op_log.debug('ignore %s' % rel_path)
            elif not os.path.isfile(abs_path):  # path
                added += int(self.add_path(abs_path, ext))
            elif validate_ext(abs_path, ext):  # file and validate
                added += int(self.add_file(abs_path))
        return added

    def save(self):
        FileMeta.mng.save()

    def get_elements(self):
        return FileMeta.mng.get_all()

    def _file_path(self, file_id):
        return os.path.join(self.repo_path, file_id)

    @classmethod
    def _build_meta(cls, src_file):
        rawname, ext = os.path.splitext(os.path.basename(src_file))
        file_id = '%s%s' % (md5_for_file(src_file), ext)
        return FileMeta(file_id, rawname)

if __name__ == '__main__':
    log.debug('debug mode begin')
    print FlatFile._build_meta(__file__) 
    test_dir = 'demo_repo'
    if os.path.exists(test_dir):
        log.debug('rm test dir %s' % test_dir)
        shutil.rmtree(test_dir)

    log.debug('cp follows by add')
    repo = FlatFile(test_dir)
    repo.add_file(__file__)
    repo.add_path('.', '*.pdf, jpg,.png,')
    repo.save()

    log.debug('add nothing')
    repo2 = FlatFile(test_dir)
    repo2.add_file(__file__)
    repo2.add_path('.', '*.pdf, jpg,.png,')
    repo.save()

    os.remove(FileMeta.mng.datafile)
    log.debug('add without cp')
    repo3 = FlatFile(test_dir)
    repo3.add_file(__file__)
    repo3.add_path('.', '*.pdf, jpg,.png,')
    repo.save()

    log.debug('debug mode end')
