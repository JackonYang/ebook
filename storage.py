# -*- coding: utf-8-*-
"""Store readonly files and file meta info based on local file

"""
import os
import codecs
import shutil
from model import BookMeta
from util.util import open_file as _open_file

def build_repo(root_path):
    """install root_path to save meta info

    """
    repo = FileStore(root_path)
    BookMeta.repo = repo
    return repo

class FileStore:

    def __init__(self, root_path):
        self.root_path = os.path.abspath(root_path)
        self.meta_path = os.path.join(self.root_path, 'f_meta')
        self.media_path = os.path.join(self.root_path, 'f_media')

        for path in [self.meta_path, self.media_path]:
            if not os.path.exists(path):
                os.makedirs(path)

        self.meta_ext = '.json'

    def load(self, file_id):
        file_id = self._fmt_metafile_path(file_id)
        with codecs.open(file_id, 'r', 'utf8') as f:
            content = f.read()
        return content

    def save(self, file_id, content):
        with codecs.open(self._fmt_metafile_path(file_id), 'w', 'utf8') as f:
            f.write(content)

    def update_on_exists(self, file_id, content, src_file):
        dst_file = self._fmt_mediafile_path(file_id)
        try:
            shutil.copy(src_file, dst_file)
            self.save(file_id, content)
        except Exception as e:
            print e
            return 1
        return 0

    def delete(self, file_id, ext):
        # delete meta file
        try:
            for filepath in [
                self._fmt_metafile_path(file_id),
                self._fmt_mediafile_path('%s%s' % (file_id, ext))
            ]:
                os.remove(filepath)
        except IOError:
            return 1
        return 0

    # ------ retrieve ----------------

    def open_file(self, file_id):
        _open_file(self._fmt_mediafile_path(file_id))

    def get_all(self):
        metafiles = os.listdir(self.meta_path)
        return [BookMeta.feed(self.load(self._fmt_metafile_path(fname)))
                for fname in metafiles]

    # ------ path handler ------------

    def meta_exists(self, file_id):
        return os.path.isfile(self._fmt_metafile_path(file_id))

    def media_exists(self, file_id):
        return os.path.isfile(self._fmt_mediafile_path(file_id))

    def _fmt_mediafile_path(self, mediafile):
        """get abspath of mediafile

        """
        return self._format_path(mediafile, self.media_path)

    def _fmt_metafile_path(self, metafile):
        """get abspath of metafile

        """
        if not metafile.endswith('.json'):  # file_id
            metafile = '%s%s' % (metafile, self.meta_ext)
        return self._format_path(metafile, self.meta_path)

    def _format_path(self, p_file, p_root):
        if not p_file.startswith(p_root):
            p_file = os.path.join(p_root, p_file)
        return p_file
