import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
repo_path = os.path.join(BASE_DIR, 'booklist')
metafile_path = os.path.join(repo_path, 'metainfo')
bookfile_path = os.path.join(repo_path, 'bookfile')
cache_path = os.path.join(repo_path, 'cache')

try:
    from local_settings import *
except:
    pass
