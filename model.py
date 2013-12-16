# -*- coding: utf-8-*-
import json
import os
import shutil
from util.wise_log import operate_log, debug_log
from util.util import md5_for_file
from util.util import timestamp

log = debug_log()
op_log = operate_log()

class FlatFile:
    def __init__(self, repo_path, idx_filename='index.json'):
        """Decouple file position and file relationship

        save all files named by md5_code.ext in one dir,
        and raw filename/display filename/status in idx_file.

        """
        if not idx_filename.endswith('.json'):
            idx_filename = '%s.json' % idx_filename
        self.repo_path = repo_path
        self.idx_file = os.path.join(repo_path, idx_filename)

        # make path if not exists
        if not os.path.exists(self.repo_path):
            os.makedirs(self.repo_path)

        if not os.path.isfile(self.idx_file):
            self.files = {}
        else: 
            with open(self.idx_file, 'r') as f:
                self.files = json.loads(f.read())

    def get_filepath(self, idx_name):
        return os.path.join(self.repo_path, idx_name)
    
    def get_filelist(self, orderby=None):
        return list(self.files.keys())

    def get_rawname(self, idx_name):
        """get raw name of a file

        return list of non-repeat raw names

        """
        if idx_name not in self.files:
            return []

        return set(list(self.files[idx_name].get('rawname', [])))

    def get_dispname(self, idx_name):
        """get display name of a file

        if display name does not exist, return list of non-repeat raw names

        """
        if idx_name not in self.files:
            return []
        try:
            return [self.files[idx_name]['dispname']]
        except KeyError:
            return self.get_rawname(idx_name)

    def update_dispname(self, idx_name, dispname):
        self.files[idx_name]['dispname'] = dispname
        self.save()

    def add_idx(self, idx_name, rawname):
        if isinstance(rawname, basestring):
            rawname = [rawname]
        if idx_name in self.files and 'rawname' in self.files[idx_name]:
            self.files[idx_name]['rawname'].extend(rawname)
        else:
            self.files[idx_name] = {'rawname': rawname}

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
        with open(self.idx_file, 'w') as f:
            f.write(json.dumps(self.files, indent=4, sort_keys=True))
        op_log.info('save idx_file')

    def backup(self, auto=True):
        if not os.path.isfile(self.idx_file):
            return 1
        prefix = 'bak'
        if auto:
            prefix = 'autobak'
        backup_file = os.path.join(self.repo_path, '%s_index_%s.json.bak' % (prefix, timestamp(for_name=True)))
        if auto:
            shutil.copy(self.idx_file, backup_file)
        else:
            shutil.move(self.idx_file, backup_file)

