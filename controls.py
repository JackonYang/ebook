# -*- coding: utf-8-*-
import os
import shutil
from model import FileMeta, MetaManager
from util.util import md5_for_file
from util.util import open_file as open_file_
from util.wise_log import operate_log, debug_log
log = debug_log()
# op_log = operate_log()

ignore_seq = {'.git', 'log'}  # read from config
def _is_ignore_path(path, ignore_hiden=True):
    if ignore_hiden and path.startswith('.'):
        return True
    if path in ignore_seq:
        return True
    return False

def validate_ext(filename, ext_range):
    ext_range = ext_range.strip(',')
    prefix, ext = os.path.splitext(filename)
    if ext.strip('.') in [item.strip('*. ') for item in ext_range.split(',')]:
        return True
    return False


class FlatFile:

    def __init__(self, repo_path, metafile='meta.json'):
        self.repo_path = repo_path
        ignore_seq.add(repo_path)
        if not os.path.exists(self.repo_path):
            os.makedirs(self.repo_path)

        self.meta_mng = MetaManager(os.path.join(self.repo_path, metafile))

    def open_file(self, file_id):
        open_file_(self._file_path(file_id))

    def add_file(self, src_file, metainfo=None, auto_save=True):
        if not os.path.isfile(src_file):
            log.error('%s not exists' % src_file)
            return False

        if metainfo is None:
            metainfo = self._build_meta(src_file)

        dst_file = self._file_path(metainfo.file_id)
        # cp src_file dst_file
        try:
            if not os.path.isfile(dst_file):
                log.debug('cp %s' % src_file)
                shutil.copy(src_file, dst_file)
            log.info('add %s' % src_file)
        except Exception as e:
            log.error('failed to copy %s. %s' % (src_file, e))
            return False
        if self.meta_mng.add(metainfo) and auto_save:
            self.meta_mng.save()
            return metainfo.file_id
        return False

    def add_path(self, src_path, ext='*.pdf', auto_save=True): 
        for rel_path in os.listdir(src_path):
            abs_path = os.path.join(src_path, rel_path)
            if os.path.isfile(abs_path):
                if validate_ext(abs_path, ext):
                    self.add_file(abs_path, auto_save=False)
            elif not _is_ignore_path(rel_path):
                self.add_path(abs_path, ext, auto_save=False)
            else:
                log.debug('ignore %s' % rel_path)
        if auto_save:
            self.meta_mng.save()

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
    repo = FlatFile(test_dir)
    log.debug('cp follows by add')
    file_id = repo.add_file(__file__)
    print file_id
    repo.add_path('.', '*.pdf, jpg,.png,')

    log.debug('add without cp')
    repo.add_path('.', '*.pdf, jpg,.png,')
    # repo.open_file(file_id)
    log.debug('debug mode begin')
