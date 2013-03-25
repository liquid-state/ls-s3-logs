import os
from setuptools import setup, find_packages


def read_file(filename):
    """Read a file into a string"""
    path = os.path.abspath(os.path.dirname(__file__))
    filepath = os.path.join(path, filename)
    try:
        return open(filepath).read()
    except IOError:
        return ''


# Hack to prevent stupid "TypeError: 'NoneType' object is not callable" error
# in multiprocessing/util.py _exit_function when running `python
# setup.py test` (see
# http://www.eby-sarna.com/pipermail/peak/2010-May/003357.html)
try:
    import multiprocessing
except ImportError:
    pass

required_packages = [
    'boto==2.8.0',
    'dateutil'
]

test_packages = [
    'pylint',
    'nose',
    'nose-testconfig==0.8',
    'coverage',
]

setup(
    name='ls-s3-logs',
    version=__import__('lss3logs').__version__,
    author='Liquid State Pty Ltd',
    author_email='dev@liquid-state.com',
    packages=find_packages(),
    url='https://github.com/liquid-state/ls-s3-logs',
    license='BSD',
    description=u' '.join(__import__('lss3logs').__doc__.splitlines()).strip(),
    classifiers=[
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Intended Audience :: Developers',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Development Status :: 4 - Beta',
        'Operating System :: OS Independent',
    ],
    long_description=read_file('README.md'),
    install_requires=required_packages,
    tests_require=required_packages + test_packages,
    test_suite='nose.collector',
)