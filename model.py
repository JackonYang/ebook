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

class Manager:
    def __init__(self, client, datafile):
        self.client = client  # model managed 
        self.datafile = datafile
        self.elements = {}
        self.load()

    def load(self, src_file=None):
        """load meta info from file
        
        """
        if src_file is None:
            src_file = self.datafile
        if os.path.isfile(src_file):
            with codecs.open(src_file, 'r', 'utf8') as f:
                eles = [self.client.parse(item) for item in json.loads(f.read(), encoding='utf8')]
            self.elements = {ele.primary_key: ele for ele in eles}

    def save(self):
        data = [unicode(ele) for ele in self.get_all()]
        data.sort()
        with codecs.open(self.datafile, 'w', 'utf8') as f:
            f.write(json.dumps(data, **_json_kwargs))

    def get_all(self):
        return list(self.elements.values())

    def add(self, ele):
        """do nothing if exists

        """
        if ele.primary_key in self.elements:
            return False
        self.elements[ele.primary_key] = ele
        return True

    def add_if_exists(self, ele, method='merge'):
        if not self.add(ele):
            meth = getattr(self.elements[ele.primary_key], method)
            meth(ele)
            return False
        return True

    def remove(self, ele):
        return self.elements.pop(ele.primary_key, None)


class FileMeta:
    """meta info of a flat file

    @attr file_id: file id, immuttable. for example: md5.ext.
    @attr rawname: set of raw filenames. support add only.
    @attr dispname: str of display name. only 1 name is supported. support update only.
    @attr status: int flat of status. support update only.
    
    """

    mng = None

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

    @property
    def primary_key(self):
        return self.file_id

    @classmethod
    def init_mng(cls, repo_name, mng=Manager):
        cls.mng = mng(FileMeta, repo_name)

    @classmethod
    def parse(cls, string):
        return FileMeta(*json.loads(string, encoding='utf8'))

    def merge(self, meta):
        # merge rawname
        self.add_rawname(meta.rawname)
        if self.dispname is None:
            self.dispname = meta.dispname

    def update(self, meta):
        self.add_rawname(meta.rawname)
        self.dispname = meta.dispname

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

    #@save_on_change
    def set_dispname(self, dispname):
        self.dispname = dispname
        if self.mng:
            self.mng.save()

    #@save_on_change
    def set_status(self, status):
        self.status = status
        if self.mng:
            self.mng.save()

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
    
    print '----------- Manager -------------'
    FileMeta.init_mng('test.json')
    obj_d = FileMeta('bbs2343.pdf', 'vivian.pdf')
    print FileMeta.mng.add(obj_a)
    print FileMeta.mng.add(obj_d)
    FileMeta.mng.save()
    print False == FileMeta.mng.add(obj_a)
    print False == FileMeta.mng.add(obj_d)
    print len(FileMeta.mng.get_all()) == 2

    for meta in FileMeta.mng.get_all():
        print unicode(meta)

    # __clear()
