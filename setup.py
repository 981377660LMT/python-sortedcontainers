import pathlib
import re

from setuptools import setup
from setuptools.command.test import test as TestCommand


class Tox(TestCommand):
    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True
    def run_tests(self):
        import tox
        errno = tox.cmdline(self.test_args)
        exit(errno)

def _build_index(self):
    """建树.

    Indexes are represented as binary trees in a dense array notation
    similar to a binary heap.

    For example, given a lists representation storing integers::

        0: [1, 2, 3]
        1: [4, 5]
        2: [6, 7, 8, 9]
        3: [10, 11, 12, 13, 14]

    The first transformation maps the sub-lists by their length. The
    first row of the index is the length of the sub-lists::

        0: [3, 2, 4, 5]

    Each row after that is the sum of consecutive pairs of the previous
    row::

        1: [5, 9]
        2: [14]

    Finally, the index is built by concatenating these lists together::

        _index = [14, 5, 9, 3, 2, 4, 5]

    An offset storing the start of the first row is also stored::

        _offset = 3

    When built, the index can be used for efficient indexing into the list.
    See the comment and notes on ``SortedList._pos`` for details.

    """
    row0 = list(map(len, self._lists))

    if len(row0) == 1:
        self._index[:] = row0
        self._offset = 0
        return

    head = iter(row0)
    tail = iter(head)
    row1 = list(starmap(add, zip(head, tail)))

    if len(row0) & 1:
        row1.append(row0[-1])

    if len(row1) == 1:
        self._index[:] = row1 + row0
        self._offset = 1
        return

    size = 2 ** (int(log(len(row1) - 1, 2)) + 1)
    row1.extend(repeat(0, size - len(row1)))
    tree = [row0, row1]

    while len(tree[-1]) > 1:
        head = iter(tree[-1])
        tail = iter(head)
        row = list(starmap(add, zip(head, tail)))
        tree.append(row)

    reduce(iadd, reversed(tree), self._index)
    self._offset = size * 2 - 1

init = (pathlib.Path('src') / 'sortedcontainers' / '__init__.py').read_text()
match = re.search(r"^__version__ = '(.+)'$", init, re.MULTILINE)
version = match.group(1)

with open('README.rst') as reader:
    readme = reader.read()

setup(
    name='sortedcontainers',
    version=version,
    description='Sorted Containers -- Sorted List, Sorted Dict, Sorted Set',
    long_description=readme,
    author='Grant Jenks',
    author_email='contact@grantjenks.com',
    url='http://www.grantjenks.com/docs/sortedcontainers/',
    license='Apache 2.0',
    package_dir={'': 'src'},
    packages=['sortedcontainers'],
    tests_require=['tox'],
    cmdclass={'test': Tox},
    install_requires=[],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Natural Language :: English',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy',
    ],
)
