import os
import json
import shutil
from util.kkfile import md5_for_file


class BookRepo:
    """
    filelist and index
    """
    def __init__(self, repo_path, backup_path=None):
        """
        init repo with path info and load index
        """
        self.repo_path = repo_path
        self.idx_file = os.path.join(repo_path, 'archive.json')
        if backup_path is None:
            backup_path =  os.path.join(self.repo_path, 'backup')
        self.backup_path = backup_path

        # make path if not exists
        for path in [backup_path, repo_path]:
            if not os.path.exists(path):
                os.makedirs(path)

        # auto load idx
        self.idx = self.__init_idx()

    def __del__(self):
        self.__save_idx()

    def __init_idx(self):
        try:
            with open(self.idx_file, 'r') as f:
                content = f.read()
        except IOError:
            content = '{}'
        else:
            # backup index file before change
            backup_file = os.path.join(self.backup_path, '%s.bak' % md5_for_file(self.idx_file))
            shutil.move(self.idx_file, backup_file)
        return json.loads(content)

    def __save_idx(self):
        import json
        with open(self.idx_file, 'w') as f:
            f.write(json.dumps(self.idx, indent=4, sort_keys=True))

    def get_book_path(self, idx_name):
        return os.path.join(self.repo_path, idx_name)


    def merge(self, new_repo_path):
        new_repo = BookRepo(new_repo_path)
        old_idx = len(self.idx)
        for bookidx, bookname in new_repo.idx.items():
            if bookidx in self.idx:
                self.idx[bookidx].append(bookname)
                print 'warning | skip cp %s ' % bookidx
            else:
                print 'cp %s' % bookname
                self.idx[bookidx] = bookname
                shutil.copy(new_repo.get_book_path(bookidx), self.repo_path)
        print '%s files merged' % (len(self.idx) - old_idx)


    def add(self, bookfile, tar_ext=''):
        if os.path.isfile(bookfile):
            orig_name, ext = os.path.splitext(os.path.basename(bookfile))
            if ext.endswith(tar_ext):
                md5 = md5_for_file(bookfile)
                md5_file = '%s%s' % (md5, ext)
                self.__add_idx(md5_file, orig_name)
                self.__add_file(bookfile, md5_file)
            else:
                print 'warning | ignore %s' % bookfile
        elif os.path.isdir(bookfile):
            for root, dirs, files in os.walk(bookfile):
                for name in dirs:
                    self.add(os.path.join(root, name), tar_ext)
                for name in files:
                    self.add(os.path.join(root, name), tar_ext)
        else:
            print 'file or path needed'

    def __add_idx(self, md5_file, orig_name):
        if md5_file in self.idx:
            self.idx[md5_file].append(orig_name)
        else:
            self.idx[md5_file] = [orig_name]

    def __add_file(self, orig_file_full, md5_file):
        # catch except when attempting to remove a file that is in use
        md5_file_full = os.path.join(self.repo_path, md5_file)
        if not os.path.isfile(md5_file_full):
            shutil.move(orig_file_full, md5_file_full)
            print 'info | mv %s' % orig_file_full
        else:
            # log it, warning
            print 'warning | rm %s' % orig_file_full
            os.remove(orig_file_full)


if __name__ == '__main__':
    repo1 = '/media/document/book_repo'
    repo2 = 'a'
    booklist = BookRepo(repo1)
    # booklist.add('/media/document/book/calibre', 'pdf')
    booklist.merge(repo2)
