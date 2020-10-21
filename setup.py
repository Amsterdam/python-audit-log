import codecs
import os
import sys

from setuptools import find_packages, setup
from setuptools.command.test import test as TestCommand


class PyTest(TestCommand):
    user_options = [('pytest-args=', 'a', "Arguments to pass to py.test")]

    def initialize_options(self):
        TestCommand.initialize_options(self)
        self.pytest_args = []

    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True

    def run_tests(self):
        # import here, cause outside the eggs aren't loaded
        import pytest
        errno = pytest.main(self.pytest_args)
        sys.exit(errno)


def read(rel_path):
    here = os.path.abspath(os.path.dirname(__file__))
    with codecs.open(os.path.join(here, rel_path), 'r') as fp:
        return fp.read()


def get_version(rel_path):
    """
    Read the package version from a single source.

    See https://packaging.python.org/guides/single-sourcing-package-version/#single-sourcing-the-package-version
    :param rel_path:
    :return:
    """
    for line in read(rel_path).splitlines():
        if line.startswith('__version_info__'):
            # transform __version_info__ = (x, y, z) to "x.y.z"
            return line.split('(')[1].split(')')[0].replace(', ', '.')
    else:
        raise RuntimeError("Unable to find version string.")


with open(os.path.join(os.path.dirname(__file__), 'README.md')) as readme:
    README = readme.read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))


install_requirements = [
]

test_requirements = [
    'pytest',
    'pytest-cov'
]

extra_requirements = {
    'dev': test_requirements + ['twine', 'bump2version'],
}



setup(
    name='datapunt-audit-log',
    version=get_version('src/audit_log/__init__.py'),
    license='Mozilla Public License 2.0',

    author='Datapunt Amsterdam',
    author_email='datapunt@amsterdam.nl',

    description='A simple python package to enable uniform audit logging',
    long_description=README,
    long_description_content_type="text/markdown",
    url='https://github.com/Amsterdam/auditlog',

    packages=find_packages(where='src'),
    package_dir={'': 'src'},
    install_requires=install_requirements,

    cmdclass={'test': PyTest},
    tests_require=test_requirements,

    extras_require=extra_requirements,

    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Framework :: Django :: 2.2',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Mozilla Public License 2.0 (MPL 2.0)',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: System :: Logging'
    ],
)
