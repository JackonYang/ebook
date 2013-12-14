import unittest
import model

import shutil
import os

repo_path = ['test_repo_exists', 'test_repo_not_exists']
# json_file = ['test_file_empty.json', 'test_file_empty_dict.json', 'test_file_not_exists.json']
json_file = ['test_file_empty_dict.json', 'test_file_not_exists.json']

def rm_repo_path():
    for path in repo_path:
        if os.path.exists(path):
            shutil.rmtree(path, ignore_errors=True)

class testBookList(unittest.TestCase):
    def setUp(self):
        rm_repo_path()
        shutil.copytree('data_unittest', 'test_repo_exists')
        
    def tearDown(self):
        rm_repo_path()

    def testInit(self):
        full_dict = {
                u'b1946ac92492d2347c6235b4d2611184.pdf': [u'test_like_pdf1', u'test_like_pdf2'],
                u'12223ae7f9bf07744445e93ac5595156.pdf': [u'test_file_not_exists'], 
                u'0f723ae7f9bf07744445e93ac5595156.pdf': [u'test_like_pdf0000']
                }
        repo = model.BookFile('test_repo_exists', 'test_file_not_empty.json')
        self.assertItemsEqual(repo.files, full_dict)

        repo = model.BookFile('test_repo_exists', 'test_file_not_empty')
        self.assertItemsEqual(repo.files, full_dict)

        for filename in json_file:
            repo = model.BookFile('test_repo_exists', filename)
            self.assertItemsEqual(repo.files, {})

        repo = model.BookFile('test_repo_not_exists', 'test_file_not_exists.json')
        self.assertItemsEqual(repo.files, {})

        repo = model.BookFile('test_repo_not_exists')
        self.assertItemsEqual(repo.files, {})

        # raise exception json file format error
        self.assertRaises(ValueError, model.BookFile, 'test_repo_exists', 'test_file_empty.json')


testCases = {testBookList('testInit')
        }

if __name__ == '__main__':
    suite=unittest.TestSuite()
    runner=unittest.TextTestRunner()
    runner.run(suite)
    for testcase in testCases:
        suite.addTest(testcase)
    runner=unittest.TextTestRunner()
    runner.run(suite)
