import unittest
import test_tools

import controls


class testViews(unittest.TestCase):
    def setUp(self):
        path, filename = test_tools.init_test_data()

    def tearDown(self):
        test_tools.clear_test_data()

    def testBuildRepo(self):
        # full filename, full data, repo exists
        full_dict = {
                u'b1946ac92492d2347c6235b4d2611184.pdf': [u'test_like_pdf1', u'test_like_pdf2', u'test_like_pdf1'],
                u'12223ae7f9bf07744445e93ac5595156.pdf': [u'test_file_not_exists'], 
                u'0f723ae7f9bf07744445e93ac5595156.pdf': [u'test_like_pdf0000']
                }
        controls.build_repo('test_repo_exists', 'test_file_not_empty.json')
        self.assertItemsEqual(controls.filelist.files, full_dict)

        # repo path not exists
        controls.build_repo('test_repo_not_exists')
        self.assertItemsEqual(controls.filelist.files, {})

        self.assertRaises(ValueError, controls.build_repo, 'test_repo_exists', 'test_file_empty.json')


testcases = {
        testViews('testBuildRepo'),
        }

if __name__ == '__main__':
    test_tools.run_tests(testcases)
