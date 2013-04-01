======================
S3 log parsing library
======================

A python library to parse S3 log files.


Warning
=======

Unit tests currently require actual S3 credentials (and a bucket with logs) and can therefore only be run manually.
Mocking the relevant parts of boto.s3 is on the roadmap. Contributions are welcome :)


Purpose
=======

Download S3 logs from a bucket, and parse them.

This application does not store the log objects generated and leaves that to other applications.


Install
=======

Eventually from pypi ...


Use
===

To get logs, simply use the Downloader class::

    from itertools import chain
    from pprint import pprint
    from lss3logs.download import Downloader

    MY_ACCESS_KEY_ID = 'XXX'
    MY_KEY_SECRET = 'XXX'
    MY_S3_BUCKET_NAME = 'XXX'

    downloader = Downloader(
        connection=None,
        aws_access_key_id=MY_ACCESS_KEY_ID,
        aws_key_secret=MY_KEY_SECRET,
    )

    # download 10 logs
    logs = downloader.download_files(
        MY_S3_BUCKET_NAME,
        prefix='logs/',
        max_logs=1)

    entries = [ log.entries for log in logs ]
    entries = list(chain.from_iterable(entries))
    [pprint(entry.__dict__) for entry in entries]


Running tests
=============

First you need to specify the test config, which contains the AWS credentials and details of bucket tot test with.
python-testconfig is used to manage the test configuration.

Copy test_config.ini.sample to test_config.ini (in the same directory) and set correct values::

    export NOSE_TESTCONFIG_AUTOLOAD_INI=`pwd`/test_config.ini

To test with nose::

    python setup.py nosetests

or running nosetests directly::

    nosetests -s --exe

Directly and with coverage::

    nosetests -s --exe --with-coverage --cover-package=lss3logs

(Note: the --exe includes python files whoch are executable, so it's optional if you don't have any.)


Code quality
============

Checking code with pylint::

    pylint lss3logs


TODO
====

* mock boto output (see https://github.com/eykd/duo/blob/master/test_duo.py for an example)
* fix as many errors as possbile reported by pylint
* bring test coverage to 100%
* use Sphinx for docs


Credits
=======

The regular expression for parsing the log lines is copied from a script by "kkowalczyk" located at http://code.google.com/p/kjk/source/browse/trunk/scripts/test_parse_s3_log.py
