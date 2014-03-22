db_ip = "localhost"
db_port = 27017
db_name = 'data_bang'
ignore_seq = {'.git', 'log', 'logs'}
media_path = "/media/document/books"

try:
    from local_settings import *
except:
    pass
