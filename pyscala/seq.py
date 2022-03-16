# 03/15/22
# Seq.py
from .iterable import *

class ConcatIterable:
    """Used as a simple stub class to allow for the inclusion of a '++' operator for concatenating
    iterables.

    Because these data structures do not hold any persistent or unique states, the original
    instance type is not needed and it will be compatible with any subclasses of `Seq`

        >>> print(List(1, 2, 3) ++ List(4, 5, 6))
        List(1, 2, 3, 4, 5, 6)
    """

    __slots__ = "set", "dat"

    def __init__(self, *dat):
        object.__setattr__(self, "set", Nil)
        self.dat = dat

    def __iter__(self):
        yield from self.dat

    def __getattribute__(self, attr):
        if attr not in ("dat", "set"):
            raise ConcatIterable.attribute_error("get")
        return object.__getattribute__(self, attr)

    def __setattr__(self, attr, value):
        if attr not in ("dat", "set") or self.set is not Nil:
            raise ConcatIterable.attribute_error("set")
        object.__setattr__(self, "set", True)
        object.__setattr__(self, attr, value)

    def attribute_error(type):
        return AttributeError(
            f"cannot {type} attribute, ConcatIterable is used for a single concatenation between iterables with '++'")

class Seq(Iterable):
    def __pos__(self):
        return ConcatIterable(*self)

    def __add__(self, item):
        items = tuple(item) if isinstance(item, ConcatIterable) else (item, )
        return self.__class__(*(tuple(self) + items))

    def __radd__(self, item):
        items = tuple(item) if isinstance(item, ConcatIterable) else (item, )
        return self.__class__(*((items + tuple(self))))

    @classmethod
    def fill(cls, n):
        def filler(item):
            return cls(*(item for _ in range(n)))
        return filler

    @property
    def reverseIterator(self):
        yield from self[::-1]

    @return_cls
    def sortWith(self, lt):
        return self.__class__(*sorted(self, key=lt))

class List(Seq):
    pass
