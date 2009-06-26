#!/usr/bin/python

# Bruno Gola
# brunogola@gmail.com - Jun, 2009
# free software

r"""

DocTest

    >>> import os
    >>> _ = os.system("rm -rf obm_*")
    >>> class Person(Obm):
    ...    fields = (
    ...            #   (field name, field type, [default]),
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

from buzhug import Base, Record

class ObmMeta(type):

    def __new__(mcls, name, bases, dic):
        if not 'fields' in dic:
            return type.__new__(ObmMeta, name, bases, dic)
        base = Base("obm_%s" % name.lower())
        fields = [ (field[0], getattr(field[1], 'bhbase', field[1])) for field in dic['fields'] ]
        dic['bhbase'] = base.create(*fields, **{'mode':'open'})
        return type.__new__(ObmMeta, name, bases, dic)

    def __getitem__(mcls, num):
        return mcls.bhbase.__getitem__(num)

    def __iter__(mcls):
        return iter(mcls.from_record(rec) for rec in mcls.bhbase)

class Obm(object):

    __metaclass__ = ObmMeta

    def __init__(self, *args, **kwargs):
        create_db = kwargs.get('create_db', True)
        for field in self.fields:
            attr = kwargs[field[0]]
            setattr(self, field[0], attr)
        if create_db:
            self.__id__ = self.bhbase.insert(**self._make_myattrs())
    
    def _make_myattrs(self):
        myattrs = {}
        for field in self.fields:
            attr = getattr(self, field[0])
            if isinstance(attr, Obm):
                myattrs[field[0]] = attr.bhbase[attr.__id__]
            else:
                myattrs[field[0]] = attr
        return myattrs

    def __setattr__(self, attr, value):
        if isinstance(value, Record):
            for field in self.fields:
                if field[0] == attr:
                    value = field[1].from_record(value)
                    break
        return object.__setattr__(self, attr, value)

    def save(self):
        myattrs = self._make_myattrs()
        for k in myattrs.keys():
            self.bhbase.update(self.get(self.__id__), **{k:myattrs[k]})
        c = self.bhbase.commit()

    @classmethod
    def from_record(cls, record):
        myattrs = {'create_db': False}
        for field in cls.fields:
            myattrs[field[0]] = getattr(record, field[0])
        instance = cls(**myattrs)
        instance.__id__ = record.__id__
        instance.__version__ = record.__version__
        return instance

    @classmethod
    def get(cls, id_):
        return cls.from_record(cls.bhbase[id_])

    def __eq__(self, other):
        return self.__id__ == other.__id__

if __name__ == '__main__':
    import doctest
    doctest.testmod()
