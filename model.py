# -*- coding: utf-8-*-
"""model for book meta info

book meta info saved in json file, 1 json file for 1 book.
@necessary attr: file_id, file_ext, rawname, dispname

abspath is used, use abspath_metafile to get abspath
input supported: file_id, json file name, abs path, BookMeta obj

install_repo before use BookMeta or BookFile

rawname is save in set and show in str.
if dispname is None, show rawname without any influence on storage.

"""
import os
import sys
import json
import codecs
import time

_root_path = None
_auto_save = True  # when setattr
_time_fmt = '%Y-%m-%d %H:%M:%S'
_json_kwargs = {'indent': 4,
                'separators': (',', ': '),
                'encoding': 'utf8',
                'sort_keys': True,
                }


def install_repo(root_path, auto_save=True):
    """install root_path to save meta info

    """
    global _root_path
    global _auto_save
    _root_path = os.path.abspath(root_path)
    if not os.path.exists(_root_path):
        os.makedirs(_root_path)
    _auto_save = auto_save


def abspath_metafile(file_id):
    if file_id.startswith(_root_path):
        return file_id
    if file_id.endswith('.json'):
        fname = file_id
    else:
        fname = '%s.json' % file_id
    return os.path.join(_root_path, fname)


def load(metafile):
    with codecs.open(abspath_metafile(metafile), 'r', 'utf8') as f:
        content = f.read()
    return BookMeta(**json.loads(content, encoding='utf8'))


def _clean_str(string):
    """convert utf8 unicode if string is str

    filesystemencoding is used to decode

    """
    if isinstance(string, str):
        string = string.decode(sys.getfilesystemencoding())
    return string


def exists(file_id):
    return os.path.isfile(abspath_metafile(file_id))


def get_all():
    return [load(fname) for fname in os.listdir(_root_path)]


class BookMeta:
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

    def save(self):
        if _root_path is None:
            raise NameError('root path for BookMeta is not defined')

        with codecs.open(abspath_metafile(self.file_id), 'w', 'utf8') as f:
            f.write(unicode(self))

    def __unicode__(self):
        obj = {'file_id': self.file_id,
               'rawname': list(self.rawname),
               'dispname': self.dispname,
               'file_ext': self.file_ext,
               }
        obj.update(self.additional)
        return json.dumps(obj, **_json_kwargs)

    def __setattr__(self, name, value, save=None):
        self.__dict__[name] = value
        if _auto_save:
            self.save()

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
    install_repo('test_repo')
    a = BookMeta(
        'hello.sfd', 'pdf', 'rawname_a', None,  # required attr
        a=4, create_time=time.time()  # additional attr
    )
    a.save()
    b = BookMeta(
        'worldccc', 'pdf', ['rawname2', 'rawname3'], 'hello world',
        sizeInBytes=1024000
    )
    b.save()
    print get_all()
    c = load('worldccc')
    print unicode(c)
    print unicode(c) == unicode(b)
    print a.get_dispname()
    print a.dispname
    print a.get_create_time()
    print b.get_create_time()
    print '%.2f(Mb)' % b.get_sizeInMb()
    print '%.2f(Mb)' % a.get_sizeInMb()
    print exists('worldccc')
    print exists('aaaaa')
