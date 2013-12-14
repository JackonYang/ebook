import unittest
import model

import shutil
import os


def rm_repo_path():
    for path in ['test_repo_exists', 'test_repo_not_exists']:
        if os.path.exists(path):
            shutil.rmtree(path, ignore_errors=True)

class testBookList(unittest.TestCase):
    def setUp(self):
        rm_repo_path()
        shutil.copytree('data_unittest', 'test_repo_exists')
        self.books = model.BookFile('test_repo_exists', 'test_file_not_empty.json')
        
    def tearDown(self):
        rm_repo_path()

    def testInit(self):
        # full filename, full data, repo exists
        full_dict = {
                u'b1946ac92492d2347c6235b4d2611184.pdf': [u'test_like_pdf1', u'test_like_pdf2', u'test_like_pdf1'],
                u'12223ae7f9bf07744445e93ac5595156.pdf': [u'test_file_not_exists'], 
                u'0f723ae7f9bf07744445e93ac5595156.pdf': [u'test_like_pdf0000']
                }
        repo = model.BookFile('test_repo_exists', 'test_file_not_empty.json')
        self.assertItemsEqual(repo.files, full_dict)

        # filename without json extension, full data, repo path exists
        repo = model.BookFile('test_repo_exists', 'test_file_not_empty')
        self.assertItemsEqual(repo.files, full_dict)

        # file not exists or empty dict in json file, repo path exists
        for filename in ['test_file_empty_dict.json', 'test_file_not_exists.json']:
            repo = model.BookFile('test_repo_exists', filename)
            self.assertItemsEqual(repo.files, {})

        # repo path not exists
        repo = model.BookFile('test_repo_not_exists', 'test_file_not_exists.json')
        self.assertItemsEqual(repo.files, {})

        # default filename
        repo = model.BookFile('test_repo_not_exists')
        self.assertItemsEqual(repo.files, {})

        # raise exception json file format error
        self.assertRaises(ValueError, model.BookFile, 'test_repo_exists', 'test_file_empty.json')

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
        self.assertItemsEqual(self.books.get_booklist(), booklist)
        repo = model.BookFile('test_repo_not_exists', 'test_file_not_exists.json')
        self.assertItemsEqual(repo.get_booklist(), [])

    def testGetOrigName(self):
        test_data = {
                u'b1946ac92492d2347c6235b4d2611184.pdf': [u'test_like_pdf1', u'test_like_pdf2'],
                u'12223ae7f9bf07744445e93ac5595156.pdf': [u'test_file_not_exists'], 
                u'0f723ae7f9bf07744445e93ac5595156.pdf': [u'test_like_pdf0000']
                }

        for idx, origname in test_data.items():
            self.assertItemsEqual(self.books.get_origname(idx), origname)

        self.assertItemsEqual(self.books.get_origname('error_idx'), [])



testCases = {testBookList('testInit'),
        testBookList('testGetFilePath'),
        testBookList('testGetBookList'),
        testBookList('testGetOrigName'),
        }


if __name__ == '__main__':
    suite=unittest.TestSuite()
    runner=unittest.TextTestRunner()
    runner.run(suite)
    for testcase in testCases:
        suite.addTest(testcase)
    runner=unittest.TextTestRunner()
    runner.run(suite)
