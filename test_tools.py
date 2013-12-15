# -*- coding: utf-8-*-
import unittest
import shutil
import os

def clear_test_data():
    for path in ['test_repo_exists', 'test_repo_not_exists', 'temp_data']:
        if os.path.exists(path):
            shutil.rmtree(path, ignore_errors=True)

def init_test_data():
    clear_test_data()
    shutil.copytree('data_unittest', 'test_repo_exists')
    shutil.copytree('data_unittest', 'temp_data')
    return ['test_repo_exists', 'test_file_not_empty.json']


def run_tests(testCases):
    suite=unittest.TestSuite()
    runner=unittest.TextTestRunner()
    for testcase in testCases:
        suite.addTest(testcase)
    runner=unittest.TextTestRunner()
    runner.run(suite)
