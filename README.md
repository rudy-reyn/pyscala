# pyscala

## Overview

I wrote up a quick port of a few of the main data structures in Scala into Python, mainly the
Iterable base class, allowing for easy subclassing for Seq and Lists, as well as other data
structures I haven't gotten around to yet.

Example usages:
```python3
>>> from pyscala import List

>>> lst = List(1, 2, 3, 4)
>>> lst2 = lst.map(lambda i: i * 2)

>>> lst; lst2
List(1, 2, 3, 4)
List(2, 4, 6, 8)

```

I implemented the `++` operator for concatenating different containers together, and opted to use
the standard addition symbol for appending items.

```python3
>>> lst ++ lst2
List(1, 2, 3, 4, 2, 4, 6, 8)

>>> lst + 5
List(1, 2, 3, 4, 5)
```


Most of the standard Iterator operations like partition, zip, foldLeft, filter, and the rest are supported.
```python3
>>> lst.zipWithIndex
List((1, 0), (2, 1), (3, 2), (4, 3))

>>>lst
List(1, 2, 3, 4)
>>> from operator import mul
>>> lst.foldLeft(2)(mul)
48
```
