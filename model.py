# -*- coding: utf-8-*-
import json
import os
import shutil

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

    def get_file_path(self, idx_name):
        return os.path.join(self.repo_path, idx_name)
