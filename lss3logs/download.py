# coding: utf-8
"""
Classes used to download a bunch of logs at once and return LogFile objects.
"""

from boto.s3.connection import S3Connection
from .log_file import LogFile


class Downloader(object):
    """
    Default class used to download log files. Return sequences of LogFile objects.
    """

    def __init__(self, 
        connection, 
        aws_access_key_id=None, 
        aws_key_secret=None):
        self.connection = connection
        self.aws_access_key_id = aws_access_key_id
        self.aws_key_secret = aws_key_secret
        self._bucket = None # caches last used S3Bucket object
        return

    def connect(self):
        """
        Creates a connection to S3 using boto.
        """
        if self.connection is not None:
            return
        self.connection = S3Connection(
            self.aws_access_key_id, 
            self.aws_key_secret)


    def get_bucket(self, bucket_name):
        """
        Returns a boto S3Bucket object.
        Caches it on the class for further reuse.
        """
        if not self._bucket or self._bucket.name != bucket_name:
            self._bucket = self.connection.get_bucket(bucket_name)
        return self._bucket


    def download_files(self, bucket_name, prefix='', max_logs=0):
        """
        Downloads all log files in a bucket at the given prefix
        """
        logs = [ ]
        self.connect()
        bucket = self.get_bucket(bucket_name)
        kwargs = { 'prefix': prefix }
        if max_logs > 0:
            kwargs['max_keys'] = max_logs
        keys = bucket.get_all_keys(**kwargs)
        for k in keys:
            logs.append(LogFile(k, prefix))
        return logs
