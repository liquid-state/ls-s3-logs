# coding: utf-8
"""
Base classes to handle reusable code for S3 connections etc.
"""

from boto.s3.connection import S3Connection


class BaseS3ConnectionHandler(object):
    """
    Base class to derive from. Handles a connection to S3.
    Allows passing an existing connection for reuse.
    """

    def __init__(self, 
        connection, 
        aws_access_key_id=None, 
        aws_key_secret=None):
        self.connection = connection
        self.aws_access_key_id = aws_access_key_id
        self.aws_key_secret = aws_key_secret
        self._bucket = None # caches last used S3Bucket object


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
