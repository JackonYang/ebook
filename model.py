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
import sys
import json
import time


_auto_save = True  # when setattr
_time_fmt = '%Y-%m-%d %H:%M:%S'
_json_kwargs = {'indent': 4,
                'separators': (',', ': '),
                'encoding': 'utf8',
                'sort_keys': True,
                }


def _clean_str(string):
    """convert utf8 unicode if string is str

    filesystemencoding is used to decode

    """
    if isinstance(string, str):
        string = string.decode(sys.getfilesystemencoding())
    return string


class BookMeta:
    """Meta info of a single book

    init a storage, and it saves data on attribute changed.

    """

    repo = None

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
    def feed(cls, content):
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
        if _auto_save and self.repo and hasattr(self.repo, 'save'):
            self.repo.save(self.file_id, unicode(self))

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

    def set_dispname(self, dispname):
        self.dispname = dispname

    def get_create_time(self):
        return time.strftime(
            _time_fmt,
            time.localtime(self._get_additional_attr('create_time', 0))
        )

    def get_sizeInMb(self):
        return self._get_additional_attr('sizeInBytes', 0) / (1024.0*1024.0)

    def get_book_version(self):
        return self._get_additional_attr('version', '')

    def set_book_version(self, version):
        return self._set_additional_attr('version', version)

    def get_book_language(self):
        return self._get_additional_attr('language', '')

    def set_book_language(self, language):
        return self._set_additional_attr('language', language)

    def _get_additional_attr(self, attr, default):
        return self.additional.get(attr, default)

    def _set_additional_attr(self, attr, value):
        self.additional[attr] = value
        if _auto_save and self.repo and hasattr(self.repo, 'save'):
            self.repo.save(self.file_id, unicode(self))


if __name__ == '__main__':
    a = BookMeta(
        'hello.sfd', 'pdf', 'rawname_a', None,  # required attr
        a=4, create_time=time.time()  # additional attr
    )
    b = BookMeta(
        'worldccc', 'pdf', ['rawname2', 'rawname3'], 'hello world',
        sizeInBytes=1024000
    )
    print unicode(a)
    print a.get_dispname()
    print a.dispname
    print a.get_create_time()
    print b.get_create_time()
    print '%.2f(Mb)' % b.get_sizeInMb()
    print '%.2f(Mb)' % a.get_sizeInMb()
