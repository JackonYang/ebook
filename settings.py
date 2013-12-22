import os

BASE_DIR = os.path.dirname(__file__)
repo_path = os.path.join(BASE_DIR, 'book_repo')
cache_path = os.path.join(BASE_DIR, 'book_cache')
log_path = os.path.join(repo_path, 'log')

from local_settings import BASE_DIR
