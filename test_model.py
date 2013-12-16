# -*- coding: utf-8-*-
import unittest
import model
import json

import shutil
import os

import test_tools


class testBookList(unittest.TestCase):
    def setUp(self):
        path, filename = test_tools.init_test_data()
        self.books = model.FlatFile(path, filename)
        
    def tearDown(self):
        test_tools.clear_test_data()

    def testInit(self):
        # full filename, full data, repo exists
        full_dict = {
                u'b1946ac92492d2347c6235b4d2611184.pdf': [u'test_like_pdf1', u'test_like_pdf2', u'test_like_pdf1'],
                u'12223ae7f9bf07744445e93ac5595156.pdf': [u'test_file_not_exists'], 
                u'0f723ae7f9bf07744445e93ac5595156.pdf': [u'test_like_pdf0000']
                }
        repo = model.FlatFile('test_repo_exists', 'test_file_not_empty.json')
        self.assertItemsEqual(repo.files, full_dict)

        # filename without json extension, full data, repo path exists
        repo = model.FlatFile('test_repo_exists', 'test_file_not_empty')
        self.assertItemsEqual(repo.files, full_dict)

        # file not exists or empty dict in json file, repo path exists
        for filename in ['test_file_empty_dict.json', 'test_file_not_exists.json']:
            repo = model.FlatFile('test_repo_exists', filename)
            self.assertItemsEqual(repo.files, {})

        # repo path not exists
        repo = model.FlatFile('test_repo_not_exists', 'test_file_not_exists.json')
        self.assertItemsEqual(repo.files, {})

        # default filename
        repo = model.FlatFile('test_repo_not_exists')
        self.assertItemsEqual(repo.files, {})

        # raise exception json file format error
        self.assertRaises(ValueError, model.FlatFile, 'test_repo_exists', 'test_file_empty.json')

    def testGetFilePath(self):
        existed_file = ['b1946ac92492d2347c6235b4d2611184.pdf', '0f723ae7f9bf07744445e93ac5595156.pdf']
        for bookfile in existed_file:
            self.assertTrue(os.path.isfile(self.books.get_filepath(bookfile)))
        not_existe_file = ['12223ae7f9bf07744445e93ac5595156.pdf']
        for bookfile in not_existe_file:
            self.assertFalse(os.path.isfile(self.books.get_filepath(bookfile)))

    def testGetBookList(self):
        booklist = ['b1946ac92492d2347c6235b4d2611184.pdf',
                '0f723ae7f9bf07744445e93ac5595156.pdf',
                '12223ae7f9bf07744445e93ac5595156.pdf']
        self.assertItemsEqual(self.books.get_filelist(), booklist)
        repo = model.FlatFile('test_repo_not_exists', 'test_file_not_exists.json')
        self.assertItemsEqual(repo.get_filelist(), [])

    def testGetOrigName(self):
        test_data = {
                u'b1946ac92492d2347c6235b4d2611184.pdf': [u'test_like_pdf1', u'test_like_pdf2'],
                u'12223ae7f9bf07744445e93ac5595156.pdf': [u'test_file_not_exists'], 
                u'0f723ae7f9bf07744445e93ac5595156.pdf': [u'test_like_pdf0000']
                }

        for idx, origname in test_data.items():
            self.assertItemsEqual(self.books.get_rawname(idx), origname)

        self.assertItemsEqual(self.books.get_rawname('error_idx'), [])

    def testAddIdx(self):

        idx_name, orig_name = [u'12223ae7f9bf07744445e93ac5595156.pdf', u'test_file_not_exists']
        self.books.add_idx(idx_name, orig_name)
        self.assertItemsEqual(self.books.get_rawname(idx_name), [orig_name])

        self.books.add_idx(idx_name, 'non-repeat-name')
        self.assertItemsEqual(self.books.get_rawname(idx_name), [orig_name, 'non-repeat-name'])

        idx_name, orig_name = [u'b1946ac92492d2347c6235b4d2611184.pdf', [u'test_like_pdf1', u'test_like_pdf2']]
        self.books.add_idx(idx_name, u'test_like_pdf2')
        self.assertItemsEqual(self.books.get_rawname(idx_name), orig_name)
        self.books.add_idx(idx_name, 'non-repeat-name')
        orig_name.append('non-repeat-name')
        self.assertItemsEqual(self.books.get_rawname(idx_name), orig_name)

    def testAddFile(self):

        src_path = 'temp_data'

        def all_exist():
            self.assertTrue(self.__file_exists(src, src_path))
            self.assertTrue(self.__file_exists(dst))

        def only_dst():
            self.assertFalse(self.__file_exists(src, src_path))
            self.assertTrue(self.__file_exists(dst))
        def only_src():
            self.assertTrue(self.__file_exists(src, src_path))
            self.assertFalse(self.__file_exists(dst))

        # new file not exists, and not del_orig
        src, dst = [u'b1946ac92492d2347c6235b4d2611184.pdf', 'new_file']
        only_src()
        self.books.add_file(os.path.join(src_path, src), dst, del_orig=False)
        all_exist()

        # new file exists, and not del_orig
        src = u'b1946ac92492d2347c6235b4d2611184.pdf'
        dst = src
        all_exist()
        self.books.add_file(os.path.join(src_path, src), dst, del_orig=False)
        all_exist()

        # new file not exists, and del_orig
        src, dst = [u'b1946ac92492d2347c6235b4d2611184.pdf', 'file_22222']
        only_src()
        self.books.add_file(os.path.join(src_path, src), dst, del_orig=True)
        only_dst()

        # new file exists, and del_orig
        src = '0f723ae7f9bf07744445e93ac5595156.pdf'
        dst = src
        all_exist()
        self.books.add_file(os.path.join(src_path, src), dst, del_orig=True)
        only_dst()

    def testSave(self):
        def parse_json(repo):
            with open(repo.idx_file, 'r') as f:
                content = f.read()
            return json.loads(content)

        repo = model.FlatFile('test_repo_exists', 'testSave001')
        repo.save()
        self.assertItemsEqual(parse_json(repo), {})

        repo.add_idx('origname', 'idxname')
        repo.save()
        self.assertItemsEqual(parse_json(repo), repo.files)

        repo.add_idx('origname2', 'idxname2')
        repo.save()
        self.assertItemsEqual(parse_json(repo), repo.files)

        repo.add_idx('origname3', 'idxname2')
        repo.save()
        self.assertItemsEqual(parse_json(repo), repo.files)

    def testBackup(self):
        self.assertTrue(self.__file_exists())  # pre check, idx_file exists

        # auto backup, keep orig file
        self.books.backup()
        self.assertTrue(self.__file_exists())

        # manual backup, remove orig file
        self.books.backup(auto=False)
        self.assertFalse(self.__file_exists())

        # return 1 if orig file not exist
        self.assertEquals(self.books.backup(), 1)  # auto check
        self.assertFalse(self.__file_exists())
        self.assertEquals(self.books.backup(auto=False), 1)  # manual check
        self.assertFalse(self.__file_exists())

    def __file_exists(self, filename=None, path=None):
        if path is None:
            path = self.books.repo_path

        if filename is None:
            src_file = self.books.idx_file
        else:
            src_file = os.path.join(path, filename)
        return os.path.isfile(src_file)

testcases = {testBookList('testInit'),
        testBookList('testGetFilePath'),
        testBookList('testGetBookList'),
        testBookList('testGetOrigName'),
        testBookList('testAddIdx'),
        testBookList('testAddFile'),
        testBookList('testSave'),
        testBookList('testBackup'),
        }

test_tools.run_tests(testcases)
