"""
termcc
-------------

This is the description for that library
"""
import os
from setuptools import setup


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


setup(
    name='logcc',
    version='2018.02.1',
    url='https://github.com/pingf/logcc.git',
    license='BSD',
    author='Jesse MENG',
    author_email='pingf0@gmail.com',
    description='log with colors',
    long_description=read('README.rst'),
    py_modules=['logcc'],
    # if you would be using a package instead use packages instead
    # of py_modules:
    packages=['logcc', 'logcc.web'],
    zip_safe=False,
    include_package_data=True,
    package_data={
        'logcc.web': ['*'],  # All files from folder A
    },
    platforms='any',
    install_requires=[
        'termcc', 'loader', 'aiohttp', 'aiofiles', 'websockets', 'pony', 'terminaltables'
    ],
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ]
)
