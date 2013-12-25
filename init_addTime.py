import time
import re
from model import FileMeta

mng = FileMeta.init_mng('../book_repo/meta.json')
ptn = re.compile(r'^(.*?),\d+\|INFO\|add (.*?\.pdf)')

def parse(t):
    return time.mktime(time.strptime(t, '%Y-%m-%d %H:%M:%S'))


with open('tt.log', 'r') as f:
    for line in f.readlines():
        try:
            t, ff = ptn.search(line).groups()
            mng.elements[ff].addtime = parse(t)
        except Exception as e:
            print line

mng.save()


