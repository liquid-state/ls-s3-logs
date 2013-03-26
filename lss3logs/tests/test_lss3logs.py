# coding: utf-8
"""
Tests for ls-s3-logs
"""

import unittest
import datetime

from testconfig import config

from lss3logs.download import Downloader
from lss3logs.delete import Deleter
from lss3logs.log_file import LogFile, LogFileEntry


class S3LogsTestCase(unittest.TestCase):
    """
    Tests everything there is about downloading log files
    """

    def __init__(self, *args, **kwargs):
        super(S3LogsTestCase, self).__init__(*args, **kwargs)
        self._downloader = None
        self._test_logs = None


    def setUp(self):
        """
        Setting up DownloaderTestCase
        """
        print 'setting up DownloaderTestCase test function'


    def _download_test_logs(self, force=False):
        """
        Downloads some log files to test with.
        This function is meant to be called by test functions.
        """
        if self._test_logs and not force:
            return self._test_logs
        aws = config['aws']
        self._downloader = Downloader(
            connection=None,
            aws_access_key_id=aws['access_key_id'],
            aws_key_secret=aws['key_secret'],
        )
        self._test_logs = self._downloader.download_files(
            aws['s3_bucket'],
            prefix=aws['logs_path'],
            max_logs=aws['max_logs_to_download'])
        return self._test_logs


    def test_downloading_logs(self):
        """
        Test downloading log files, 
        and getting back LogFile objects.
        """
        self._download_test_logs()
        self.assertTrue(
            len(self._test_logs) > 0, 
            'cannot test without logs')
        first_log = self._test_logs[0]
        self.assertIsInstance(
            first_log, LogFile, 
            'should return LogFile objects')
        self.assertIsInstance(
            first_log.log_id, unicode, 
            'log id should be a string')
        self.assertTrue(
            len(first_log.log_id) > 0, 
            'log id should not be an empty string')
        self.assertIsInstance(
            first_log.creation_datetime, datetime.datetime, 
            'log creation datetime should be a datetime object')


    def test_parsing_logs(self):
        """
        Test parsing log files, 
        and getting back LogFileEntry objects.
        """
        self._download_test_logs()
        entries = self._test_logs[0].entries
        self.assertTrue(
            len(entries) > 0, 
            'log should contain entries')
        self.assertIsInstance(
            entries[0], LogFileEntry, 
            'log entry should be a LogFileEntry object')


    def test_deleting_logs_using_keys(self):
        """
        Test deleting logs, checking that if 
        we download again we get different ones.
        This test uses keys still in memory from 
        when the logs were saved.
        """
        self._download_test_logs()
        self.assertTrue(
            len(self._test_logs) > 1, 
            'more than 1 log file are needed to test deletion')
        first_log_file = self._test_logs[0]
        first_log_id = first_log_file.log_id
        first_log_file.delete()
        self._download_test_logs(force=True)
        self.assertNotEqual(
            first_log_id,
            self._test_logs[0].log_id, 
            'first log file still present when it should have been deleted')


    def test_deleting_logs_using_deleter(self):
        """
        Test deleting logs, checking that if 
        we download again we get different ones.
        This test uses the Deleter class, for when 
        we don't have boto Key objects anymore.
        """
        self._download_test_logs()
        self.assertTrue(
            len(self._test_logs) > 1, 
            'more than 1 log file are needed to test deletion')
        first_log_file = self._test_logs[0]
        first_log_id = first_log_file.log_id

        # we use the key object's name directly here for convenience
        # but we can imagine it's been saved and retrieved 
        # from a database or such
        key_names = (first_log_file.key.name,)
        deleter = Deleter(self._downloader.connection)
        # import pdb; pdb.set_trace()
        deleter.delete_files(
            config['aws']['s3_bucket'],
            key_names,
            prefix=config['aws']['logs_path'])

        self._download_test_logs(force=True)
        self.assertNotEqual(
            first_log_id,
            self._test_logs[0].log_id, 
            'first log file still present when it should have been deleted')

