import os

BASE_DIR = os.path.dirname(__file__)
repo_path = os.path.join(BASE_DIR, 'book_repo')
cache_path = os.path.join(BASE_DIR, 'book_cache')
log_path = os.path.join(repo_path, 'log')

ignore_seq = {'.git', 'log'}  # read from config

try:
    from local_settings import *
except:
    pass
