# coding: utf-8
"""
Default log file class representing a single log file as created by S3.
"""

import re
import datetime
from dateutil.parser import parse as dateutil_parse


LINE_REGEX_STRING  = r'(\S+) (\S+) \[(.*?)\] (\S+) (\S+) ' \
           r'(\S+) (\S+) (\S+) "([^"]+)" ' \
           r'(\S+) (\S+) (\S+) (\S+) (\S+) (\S+) ' \
           r'"([^"]+)" "([^"]+)" (\S+)'
LINE_REGEX_COMPILED = re.compile(LINE_REGEX_STRING)


class LogFile():
    """
    Base class to represent S3 log files.
    """    

    def __init__(self, key, prefix):
        self.key = key
        self._raw_contents = None
        self._entries = None
        object_name = key.name.replace(prefix, '')
        parts = object_name.split('-')
        self.log_id = parts.pop(-1)
        parts = map(lambda p: int(p), parts)
        self.creation_datetime = datetime.datetime(*parts)


    @property
    def raw_contents(self):
        """
        Property returning the exact S3 log file string contents.
        """
        if not self._raw_contents:
            self._raw_contents = self.key.get_contents_as_string()
        return self._raw_contents


    @property
    def entries(self):
        """
        List of LogFileEntry objects parsed from self.raw_contents.
        """
        if not self._entries:
            self._entries = [
                LogFileEntry(l, self) 
                for l in self.raw_contents.splitlines() ]
        return self._entries


class LogFileEntry():
    """
    A single entry (line) in an S3 log file.
    """

    FIELD_NAMES = ('bucket_owner', 'bucket', 'datetime', 'ip', 'requestor_id', 
    'request_id', 'operation', 'key', 'http_method_uri_proto', 'http_status', 
    's3_error', 'bytes_sent', 'object_size', 'total_time', 'turn_around_time',
    'referer', 'user_agent', 'version_id')

    def __init__(self, line, log_file):
        self.line = line
        # keep track of which log file this entry came from
        self.log_id = log_file.log_id
        self.parse()

    def parse(self):
        match = LINE_REGEX_COMPILED.match(self.line)
        values = [match.group(1+n) for n in range(18)]
        for (name, value) in zip(self.FIELD_NAMES, values):
            setattr(self, name, value)
        # fix : separating date and time instade of space
        # so that the default dateutil parser can parse it
        self.datetime = self.datetime.replace(':', ' ', 1)
        self.datetime = dateutil_parse(self.datetime)
        return self
