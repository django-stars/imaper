# -*- coding: utf-8 -*-
from fabric.operations import local


def requirements(group=None):
    """Installs all of the requirements for the given group"""
    if group is None:
        local('pip install -r requirements.txt')
    elif group == 'docs':
        local('pip install Sphinx==1.2b1')
    else:
        print 'Invalid requirements group.'


def gendocs():
    """Generates the docs"""
    local('sphinx-build -b singlehtml docs docs/_build')
    print('Documentation is now available in ./docs/_build.')


def regenrst():
    """Regenerates the RST docs"""
    local('rm -f docs/imaper.rst')
    local('sphinx-apidoc -F -o docs imaper')
