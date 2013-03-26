# coding: utf-8
"""
Code used to delete S3 files.
"""

from .base import BaseS3ConnectionHandler
from .log_file import LogFile


class Deleter(BaseS3ConnectionHandler):
    """
    Simple class used to delete log files.
    """

    def __init__(self, *args, **kwargs):
        super(Deleter, self).__init__(*args, **kwargs)


    def delete_files(self, bucket_name, key_names, prefix=''):
        """
        Deletes a list of files from a bucket.
        """
        self.connect()
        bucket = self.get_bucket(bucket_name)
        for key_name in key_names:
            name = key_name \
                if key_name.startswith(prefix) \
                else prefix + key_name
            bucket.delete_key(name)
