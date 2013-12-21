"""manage a series of file metas base on file-storage

@method add: add one file meta. ignore if exists.
@method get_filemeta: return a list of corresponding file metas.
@method load: load file meta for file
@method save: save file meta to file

"""
import json
import os

metafile = None
metainfo = None

def build_repo(filename='meta.json'):
    global metafile
    global metainfo
    metafile = filename
    metainfo = {meta.file_id: meta for meta in load(metafile)}  # load meta info from file

def add(meta):
    # ignore if exists
    if meta.file_id in metainfo:
        return False
    metainfo[meta.file_id] = meta
    return True

def get_filemeta(file_ids=None):
    if file_ids is None:
        return list(metainfo.values())
    elif isinstance(file_ids, basestring):
        file_ids = [file_ids]
    return [metainfo[file_id] for file_id in file_ids]

def load(metafile):
    metas = []
    if os.path.isfile(metafile):
        with open(metafile, 'r') as f:
            metas = [FileMeta.parse(item) for item in json.loads(f.read())]
    return metas

def save():
    with open(metafile, 'w') as f:
        f.write(
                json.dumps([str(meta) for meta in get_filemeta()],
                           indent=4,
                           sort_keys=True)
                )

def __clear():
    metainfo = {}
    if os.path.isfile(metafile):
        os.remove(metafile)


class FileMeta:
    """meta info of a flat file
    
    @attr file_id: file id, immuttable. for example: md5.ext.
    @attr rawname: set of raw filenames. support add only.
    @attr dispname: str of display name. only 1 name is supported. support update only.
    @attr status: int flat of status. support update only.
    
    """

    def __init__(self, file_id, rawname, dispname=None, status=1):
        self.file_id = file_id
        if isinstance(rawname, basestring):
            self.rawname = {rawname}
        else:
            self.rawname = set(rawname)
        self.dispname = dispname
        self.status = status

    def get_dispname(self):
        if not self.dispname:
            return ','.join(self.rawname)
        return self.dispname

    def set_dispname(self, dispname):
        self.dispname = dispname
        save()

    def get_rawname(self):
        return ','.join(self.rawname)

    def add_rawname(self, rawname):
        self.rawname.add(rawname)

    def update_dispname(self, dispname):
        self.dispname = dispname

    def update_status(self, status):
        self.status= status

    @classmethod
    def parse(cls, str):
        return FileMeta(*json.loads(str))

    def __str__(self):
        return json.dumps([self.file_id, list(self.rawname), self.dispname, self.status])


if __name__ == '__main__':
    print '----------- FileMeta -------------'
    obj_a = FileMeta('aas2342.pdf', 'hello.pdf')
    obj_a.update_status(2)
    obj_a.update_dispname('hello world.pdf')
    obj_a.add_rawname('world.pdf')

    str_obj_a = str(FileMeta(*json.loads(str(obj_a))))

    obj_b = FileMeta('aas2342.pdf', ['hello.pdf', 'world.pdf', 'hello.pdf'], 'hello world.pdf', 2)
    obj_c = FileMeta.parse(str_obj_a)

    print str_obj_a == str(obj_b)
    print str(obj_b) == str(obj_c)
    
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
        print mng

    __clear()
