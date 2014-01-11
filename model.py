# -*- coding: utf-8-*-
"""model for book meta info

book meta info saved in json file, 1 json file for 1 book.
@necessary attr: file_id, file_ext, rawname, dispname

abspath is used by default, use filepath to get path
input supported: file_id, json file name, abs path

init_mng before use BookMeta or BookFile

rawname is save in set and show in str.
if dispname is None, show rawname without any influence on storage.

"""
import os
import sys
import json
import codecs
import time


_auto_save = True  # when setattr
_use_abs_path = True
_time_fmt = '%Y-%m-%d %H:%M:%S'
_json_kwargs = {'indent': 4,
                'separators': (',', ': '),
                'encoding': 'utf8',
                'sort_keys': True,
                }


def init_mng(root_path):
    """install root_path to save meta info

    """
    if _use_abs_path:
        root_path = os.path.abspath(root_path)
    if not os.path.exists(root_path):
        os.makedirs(root_path)
    mng = MetaMng(root_path)
    BookMeta.mng = mng
    return mng


def _clean_str(string):
    """convert utf8 unicode if string is str

    filesystemencoding is used to decode

    """
    if isinstance(string, str):
        string = string.decode(sys.getfilesystemencoding())
    return string


class MetaMng:

    def __init__(self, meta_root):
        self.meta_root = meta_root

    def filepath(self, metafile):
        """get abspath of metafile

        @para metafile: string is required. abspath/json file/file_id is OK.

        """
        if metafile.startswith(self.meta_root):
            return metafile
        if not metafile.endswith('.json'):  # file_id
            metafile = '%s.json' % metafile
        return os.path.join(self.meta_root, metafile)

    def load(self, filename):
        with codecs.open(filename, 'r', 'utf8') as f:
            content = f.read()
        return BookMeta.parse(content)

    def save(self, meta_obj):
        with codecs.open(self.filepath(meta_obj.file_id), 'w', 'utf8') as f:
            f.write(unicode(meta_obj))

    def meta_exists(self, file_id):
        return os.path.isfile(self.filepath(file_id))

    def get_all(self):
        metafiles = os.listdir(self.meta_root)
        return [self.load(self.filepath(fname)) for fname in metafiles]


class BookMeta:
    """Meta info of a single book

    init a manager, and it saves data once attribute changed.

    """

    mng = None

    def __init__(self, file_id, file_ext, rawname, dispname, **additional):
        # make sure that all inputs are utf-8 encoding
        self.__dict__['file_id'] = _clean_str(file_id)
        self.__dict__['file_ext'] = _clean_str(file_ext)
        self.__dict__['dispname'] = _clean_str(dispname)

        rawname = _clean_str(rawname)
        if isinstance(rawname, unicode):
            self.__dict__['rawname'] = {rawname}
        else:
            self.__dict__['rawname'] = set(rawname)

        self.__dict__['additional'] = {
            _clean_str(key): _clean_str(value)
            for key, value in additional.items()
        }

    @classmethod
    def parse(cls, content):
        """unicode str to obj"""
        return BookMeta(**json.loads(content, encoding='utf8'))

    def __unicode__(self):
        """obj to unicode str"""
        obj = {'file_id': self.file_id,
               'rawname': list(self.rawname),
               'dispname': self.dispname,
               'file_ext': self.file_ext,
               }
        obj.update(self.additional)
        return json.dumps(obj, **_json_kwargs)

    def __setattr__(self, name, value):
        self.__dict__[name] = value
        if _auto_save and self.mng and hasattr(self.mng, 'save'):
            self.mng.save(self)

    def get_rawname(self):
        return ','.join(self.rawname)

    def add_rawname(self, rawname):
        rawname = _clean_str(rawname)
        if isinstance(rawname, unicode):
            rawname = {rawname}
        self.rawname.update(rawname)

    def get_dispname(self):
        if not self.dispname:
            return self.get_rawname()
        return self.dispname

    def get_create_time(self):
        return time.strftime(
            _time_fmt,
            time.localtime(self._get_additional_attr('create_time', 0))
        )

    def get_sizeInMb(self):
        return self._get_additional_attr('sizeInBytes', 0) / (1024.0*1024.0)

    def _get_additional_attr(self, attr, default):
        return self.additional.get(attr, default)


if __name__ == '__main__':
    mng = init_mng('test_repo')
    a = BookMeta(
        'hello.sfd', 'pdf', 'rawname_a', None,  # required attr
        a=4, create_time=time.time()  # additional attr
    )
    a.mng.save(a)
    b = BookMeta(
        'worldccc', 'pdf', ['rawname2', 'rawname3'], 'hello world',
        sizeInBytes=1024000
    )
    mng.save(b)
    print mng.get_all()
    c = mng.load(mng.filepath('worldccc'))
    print unicode(c)
    print unicode(c) == unicode(b)
    print a.get_dispname()
    print a.dispname
    print a.get_create_time()
    print b.get_create_time()
    print '%.2f(Mb)' % b.get_sizeInMb()
    print '%.2f(Mb)' % a.get_sizeInMb()
    print mng.meta_exists('worldccc')
    print mng.meta_exists('aaaaa')
