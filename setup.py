from setuptools import setup, find_packages
import sys, os

version = '0.1'

setup(
    name='routr-dsl',
    version=version,
    description='DSL for defining routes',
    author='Andrey Popp',
    author_email='8mayday@gmail.com',
    url='http://routr.readthedocs.org/',
    license='BSD',
    py_modules=['routrdsl'],
    install_requires=[
        'routr >= 0.6.2',
        'routrschema >= 0.1',
    ],
    include_package_data=True,
    zip_safe=False)
