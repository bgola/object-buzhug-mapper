#!/usr/bin/python

# Bruno Gola
# brunogola@gmail.com - Jun, 2009
# free software - GPLv3

"""
DocTest

    >>> class Person(Obm):
    ...    fields = (
    ...                ('name', str),
    ...                ('age', int),
    ...             )
    ...    def __repr__(self):
    ...        return self.name
    ...    def has_a_bike(self):
    ...        return bool([b for b in Bicycle if b.owner == self ])
    >>> class Bicycle(Obm):
    ...     fields = (
    ...                ('owner', Person),
    ...              )
    ...     def __repr__(self):
    ...         return "Bicicleta d@ %s" % (self.owner)
    >>> b = Person(name="Bruno", age=21)
    >>> b.__id__
    0
    >>> c = Person(name="David", age=25)
    >>> c.__id__
    1
    >>> d = Person(name="Di", age=24)
    >>> bb = Bicycle(owner=b)
    >>> bb2 = Bicycle(owner=b)
    >>> print bb.owner
    Bruno
    >>> bbs = [ b for b in Bicycle if b.owner.name == "Bruno" ]
    >>> len(bbs)
    2
    >>> print bbs[0]
    Bicicleta d@ Bruno
    >>> di = Person.get(d.__id__)
    >>> print di
    Di
    >>> id(di) == id(d)
    False
    >>> di == d
    True
    >>> di.name = "Diana"
    >>> di.save()
    >>> Person.get(2)
    Diana
    >>> di.has_a_bike()
    False
    >>> bd = Bicycle(owner=di)
    >>> di.has_a_bike()
    True
"""

import os, sys
dirname = os.path.dirname
path = os.path.realpath(dirname(dirname(__file__)))
sys.path.append(path)
os.chdir("%s/tests/" % path)

from obm import Obm

import doctest
doctest.testmod()
os.system("rm -rf obm_*")
