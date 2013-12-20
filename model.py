import json


class FlatFile:
    """Flat File meta
    
    @attr file_id: file id. md5.ext. immuttable;
    @attr rawnames: set of raw filenames. support add only;
    @attr dispname: str of display name. only 1 name is supported. support update only;
    @attr status: int flat of status. support update only.
    
    """

    def __init__(self, file_id, rawname, dispname=None, status=1):
        self.file_id = file_id
        if isinstance(rawname, basestring):
            self.rawnames = {rawname}
        else:
            self.rawnames = set(rawname)
        self.dispname = dispname
        self.status = status

    def get_dispname(self):
        if not self.dispname:
            return ','.join(self.rawname)
        return self.dispname

    def add_rawname(self, rawname):
        self.rawnames.add(rawname)

    def update_dispname(self, dispname):
        self.dispname = dispname

    def update_status(self, status):
        self.status= status

    def __str__(self):
        return json.dumps([self.file_id, list(self.rawnames), self.dispname, self.status])

if __name__ == '__main__':
    obj_a = FlatFile('aas2342.pdf', 'hello.pdf')
    print obj_a
    obj_a.update_status(2)
    obj_a.update_dispname('hello world.pdf')
    obj_a.add_rawname('world.pdf')

    new_obj_a = str(FlatFile(*json.loads(str(obj_a))))

    obj_b = FlatFile('aas2342.pdf', ['hello.pdf', 'world.pdf', 'hello.pdf'], 'hello world.pdf', 2)
    print new_obj_a
    print new_obj_a == str(obj_b)
