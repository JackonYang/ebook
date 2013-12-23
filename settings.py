import os

BASE_DIR = os.path.dirname(__file__)
repo_path = os.path.join(BASE_DIR, 'book_repo')
to_add = ['/media/document/lean-read/media/books',
          '/media/document/book/calibre',
          '/media/document/downloads',
          ]
op_log_path = os.path.join(repo_path, 'log')  # operate log
metafile = 'meta.json'

ignore_seq = {'.git', 'log'}  # read from config

try:
    from local_settings import *
except:
    pass
