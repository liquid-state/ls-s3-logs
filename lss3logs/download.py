# coding: utf-8
"""
Classes used to download a bunch of logs at once and return LogFile objects.
"""

from .base import BaseS3ConnectionHandler
from .log_file import LogFile


class Downloader(BaseS3ConnectionHandler):
    """
    Default class used to download log files. Return sequences of LogFile objects.
    """

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
