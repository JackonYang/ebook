# -*- coding: utf-8-*-
import json
import os
import shutil
from util.wise_log import operate_log, debug_log
from util.util import md5_for_file
from util.util import timestamp

log = debug_log()
op_log = operate_log()

class BookFile:
    def __init__(self, repo_path, filename='origname.json'):
        """
        data model for file list and it orig names.
        """
        if not filename.endswith('.json'):
            filename = '%s.json' % filename
        self.repo_path = repo_path
        self.datafile = os.path.join(repo_path, filename)

        # make path if not exists
        if not os.path.exists(self.repo_path):
            os.makedirs(self.repo_path)

        if not os.path.isfile(self.datafile):
            self.files = {}
        else: 
            with open(self.datafile, 'r') as f:
                self.files = json.loads(f.read())

    def get_filepath(self, idx_name):
        return os.path.join(self.repo_path, idx_name)
    
    def get_booklist(self, orderby=None):
        return list(self.files.keys())

    def get_origname(self, idx_name):
        """
        get list of non-repeat origname.
        return [] if idx_name does not exists.
        """
        return list(set(self.files.get(idx_name, [])))

    def add_idx(self, idx_name, orig_name):
        if idx_name in self.files:
            self.files[idx_name].append(orig_name)
            op_log.info('add orig_name %s as %s' % (orig_name, idx_name))
        else:
            self.files[idx_name] = [orig_name]
            op_log.info('init orig_name %s as %s' % (orig_name, idx_name))

    def add_file(self, src_file, dst_filename, del_orig=True):
        dst_file = os.path.join(self.repo_path, dst_filename)
        if not os.path.isfile(dst_file):  # dst file exists, no move
            try:  # catch except when attempting to remove a file that is in use
                shutil.copy(src_file, dst_file)
            except:
                op_log.error('failed to add %s to BookList' % src_file)
                return False
            else:
                op_log.info('add %s to BookList as %s' % (src_file, dst_filename))
        else:
            op_log.info('file %s exists in BookList, skip copying %s' % (dst_filename, src_file))
        if del_orig:
            try:
                os.remove(src_file)
            except:
                log.error('failed to rm %s' % src_file)
            else:
                log.info('rm %s' % src_file)
        
        return True

    def save(self):
        with open(self.datafile, 'w') as f:
            f.write(json.dumps(self.files, indent=4, sort_keys=True))
        op_log.info('save datafile')

    def backup(self, auto=True):
        if not os.path.isfile(self.datafile):
            return 1
        prefix = 'bak'
        if auto:
            prefix = 'autobak'
        backup_file = os.path.join(self.repo_path, '%s_index_%s.json.bak' % (prefix, timestamp(for_name=True)))
        if auto:
            shutil.copy(self.datafile, backup_file)
        else:
            shutil.move(self.datafile, backup_file)

