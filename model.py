# -*- coding: utf-8-*-
"""manage a series of file metas base on file-storage

@method add: add one file meta. ignore if exists.
@method get_filemeta: return a list of corresponding file metas.
@method load: load file meta for file
@method save: save file meta to file

"""
import json
import os
import codecs

_json_kwargs = {'indent': 4,
                'separators': (',', ': '),
                'encoding': 'utf8',
                'sort_keys': True,
               }

metafile = None
metainfo = None
auto_save = True


def build_repo(filename='meta.json'):
    global metafile
    global metainfo
    metafile = filename
    metainfo = {meta.file_id: meta for meta in load(metafile)}  # load meta info from file

def update_if_exists(meta):
    if not add(meta):
        obj = metainfo[meta.file_id]
        obj.add_rawname(meta.rawname)
        return False
    return True

def add(meta):
    # ignore if exists
    if meta.file_id in metainfo:
        return False
    metainfo[meta.file_id] = meta
    return True

def get_filemeta():
    return list(metainfo.values())

def load(metafile):
    metas = []
    if os.path.isfile(metafile):
        with codecs.open(metafile, 'r', 'utf8') as f:
            metas = [FileMeta.parse(item) for item in json.loads(f.read(), encoding='utf8')]
    return metas

def save():
    with codecs.open(metafile, 'w', 'utf8') as f:
        f.write(json.dumps([unicode(meta) for meta in get_filemeta()], **_json_kwargs))

def __clear():
    metainfo = {}
    if os.path.isfile(metafile):
        os.remove(metafile)

def save_on_change(func):
    def _save_on_change(*args, **kwargs):
        ret = func(*args, **kwargs)
        if metafile:
            save()
        return ret
    return _save_on_change


class FileMeta:
    """meta info of a flat file

    @attr file_id: file id, immuttable. for example: md5.ext.
    @attr rawname: set of raw filenames. support add only.
    @attr dispname: str of display name. only 1 name is supported. support update only.
    @attr status: int flat of status. support update only.
    
    """

    def __init__(self, file_id, rawname, dispname=None, status=1):
        self.file_id = file_id
        if isinstance(rawname, str):
            self.rawname = {rawname.decode('utf8')}
        elif isinstance(rawname, unicode):
            self.rawname = {rawname}
        else:
            self.rawname = set(rawname)
        self.dispname = dispname
        self.status = status

    @classmethod
    def parse(cls, string):
        return FileMeta(*json.loads(string, encoding='utf8'))

    def get_dispname(self):
        if not self.dispname:
            return self.get_rawname()
        return self.dispname

    def get_rawname(self):
        # print self.rawname
        return ','.join(self.rawname)

    def add_rawname(self, rawname):
        if isinstance(rawname, str):
            rawname = {rawname.decode('utf8')}
        elif isinstance(rawname, unicode):
            rawname = {rawname}
        self.rawname.update(rawname)

    @save_on_change
    def set_dispname(self, dispname):
        self.dispname = dispname

    @save_on_change
    def set_status(self, status):
        self.status = status

    def __unicode__(self):
        return json.dumps([self.file_id, list(self.rawname), self.dispname, self.status], encoding='utf8')


if __name__ == '__main__':
    print '----------- FileMeta -------------'
    obj_a = FileMeta('aas2342.pdf', 'hello.pdf')
    obj_a.set_status(2)
    obj_a.set_dispname('hello world.pdf')
    obj_a.add_rawname(u'世界.pdf')

    obj_b = FileMeta('aas2342.pdf', ['hello.pdf', '世界.pdf', 'hello.pdf'], 'hello world.pdf', 2)

    str_obj_a = unicode(FileMeta(*json.loads(unicode(obj_a))))
    obj_c = FileMeta.parse(str_obj_a)

    print str_obj_a
    print unicode(obj_c) == str_obj_a
    
    print '----------- MetaManager -------------'
    build_repo()
    obj_d = FileMeta('bbs2343.pdf', 'vivian.pdf')
    print add(obj_a)
    print add(obj_d)
    save()
    print False == add(obj_a)
    print False == add(obj_d)
    print len(get_filemeta()) == 2

    for mng in get_filemeta():
        print unicode(mng)

    __clear()
