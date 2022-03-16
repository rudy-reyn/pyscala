# 03/15/22
# Iterable.py
from functools import wraps

class View(tuple):
    __slots__ = ()
    def __new__(cls, items):
        return tuple.__new__(cls, items)

    def __repr__(self):
        return f"View{tuple(self)}"

def singleton(cls):
    return cls()

@singleton
class Nil:
    __slots__ = ()
    def __repr__(self):
        return "Nil"
    def __bool__(self):
        return False

def return_cls(func):
    @wraps(func)
    def wrapper(cls, *args, **kwargs):
        return cls.__class__(*func(cls, *args, **kwargs))
    return wrapper

class Iterable(tuple):
    def __new__(cls, *data):
        return tuple.__new__(cls, data)

    def __repr__(self):
        return f"{self.__class__.__name__}{tuple(self)}"

    def __call__(self, index):
        return self[index]

    def __eq__(self, value):
        return tuple(self) == value


    def init(self, iterable):
        return self.__class__(*iterable)

    @return_cls
    def concat(A, B):
        return tuple(A) + tuple(B)

    def contains(self, elem):
        return elem in self

    def corresponds(A, B):
        def wrapper(p):
            return len(A) == len(B) and A.zip(B).forall(lambda ab: p(ab[0], ab[1]))
        return wrapper

    @return_cls
    def drop(self, n):
        return self.slice(0, n)

    @return_cls
    def dropRight(self, n):
        return self.slice(self.size - n, self.size)

    @return_cls
    def dropWhile(xs, predicate):
        if xs.isEmpty:
            return Seq()
        x, *xs = xs
        try:
            while(predicate(x)):
                x, *xs = xs
        except StopIteration:
            return xs
        else:
            return (x, *xs)

    @property
    def empty(self):
        return self.__class__()

    def exists(self, predicate):
        return any(predicate(x) for x in self)

    @return_cls
    def filter(self, predicate):
        return filter(predicate, self)

    @return_cls
    def filterNot(self, predicate):
        return filter(lambda x: not predicate(x), self)

    def find(self, predicate):
        return self.dropWhile(lambda x: not predicate(x)).head

    @property
    def flatten(self):
        if self.isEmpty:
            return self
        return self.foldLeft(self.empty)(
                lambda flat, elm:(
                    flat + elm.flatten if isinstance(elm, Iterable) else flat + (elm, )))

    def fold(self, seed):
        return self.foldLeft(seed)

    def foldLeft(self, seed):
        def folder(func):
            nonlocal seed
            for i in self:
                seed = func(seed, i)
            return seed
        return folder

    def foldRight(self, seed):
        def folder(func):
            nonlocal seed
            for i in self.reverse:
                seed = func(i, seed)
            return seed
        return folder

    def forall(self, p):
        return all(p(x) for x in self)

    # TODO: groupby

    @property
    def head(self):
        return self[0]

    @property
    def headOption(self):
        if not self:
            return
        return self.head

    @property
    def isEmpty(self):
        return len(self) == 0

    def last(self):
        return self[self.size - 1]

    def lastOption(self):
        if not self:
            return
        return self[self.size - 1]

    @return_cls
    def map(self, f):
        return map(f, self)

    def max(self, key=None):
        if self.isEmpty:
            raise ValueError("cannot find max of empty iterable")
        return max(self, key=key)

    def min(self, key):
        if self.isEmpty:
            raise ValueError("cannot find min of empty iterable")
        return min(self, key=key)

    def mkString(self, sep="", start="", end=""):
        return start + sep.join(self.map(str)) + end

    # partitionMap, product
    @return_cls
    def partition(self, p):
        return self.filter(p), self.filterNot(p)

    def reduce(self, op):
        return self.tail.foldLeft(self.head)(op)

    def reduceLeft(self, op):
        return self.reduce(op)

    def reduceRight(self, op):
        return self.reverse.tail.foldRight(self.last)(op)

    def reduceOption(self, op):
        if not self:
            return
        return self.reduce(op)

    def reduceLeftOption(self, op):
        if not self:
            return
        return self.reduce(op)

    def reduceRightOption(self, op):
        if not self:
            return
        return self.reduceRight(op)

    @property
    def reverse(self):
        return self.init(self[::-1])

    @property
    def size(self):
        return len(self)

    @return_cls
    def slice(self, *args):
        return self[slice(*args)]

    @property
    def sum(self):
        return sum(self)

    @property
    def tail(self):
        return self.init(self[1:])

    @return_cls
    def take(self, n):
        return self[:n]

    @return_cls
    def takeRight(self, n):
        return self[n:]

    @return_cls
    def takeWhile(self, predicate):
        if self.isEmpty:
            return Seq()
        seq = []
        x, *xs = self
        while(predicate(x)):
            seq.append(x)
            x, *xs = xs
        return seq

    @property
    def unzip(self):
        left, right = [], []
        for l, r in self:
            left.append(l)
            right.append(r)
        cls = self.__class__
        return cls(cls(*left), cls(*right))

    @property
    def unzip3(self):
        left, middle, right = [], []
        for l, m, r in self:
            left.append(l)
            middle.append(m)
            right.append(r)
        cls = self.__class__
        return cls(cls(*left), cls(*middle), cls(*right))

    @return_cls
    def zip(self, iterable):
        return zip(self, iterable)

    @property
    def zipWithIndex(self):
        cls = self.__class__
        return cls(*((v, i) for i, v in enumerate(self)))
