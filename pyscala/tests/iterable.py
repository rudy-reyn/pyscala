#!/usr/bin/env python3
# 03/15/22
# metaclasses.py
# rudy@metaclasses
import pytest
from .. import Iterable

@pytest.fixture
def lst():
   return Iterable(1, 2, 3, 4)

@pytest.fixture
def lst1():
   return Iterable("a", "b", "c", "d")

@pytest.fixture
def is_even():
    return lambda n: n % 2 == 0

def test_isinstance_tuple(lst):
    assert isinstance(lst, tuple)

def test_call_syntax(lst):
    assert lst(0) == 1
    assert lst(1) == 2
    assert lst(2) == 3
    assert lst(3) == 4

def test_eq(lst):
    assert lst == (1, 2, 3, 4)

def test_concat(lst, lst1):
    assert lst.concat(lst1) == Iterable(1, 2, 3, 4, "a", "b", "c", "d")
    assert lst1.concat(lst) == Iterable("a", "b", "c", "d", 1, 2, 3, 4)

def test_contains(lst):
    assert lst.contains(3)

def test_empty(lst):
    assert lst.empty == ()

def test_exists(lst, lst1):
    assert lst.exists(lambda i: i == 1)
    assert not lst.exists(lambda i: i == 5)
    assert lst1.exists(lambda i: isinstance(i, str))

def test_filter(lst):
    assert lst.filter(lambda i: i % 2 == 0) == (2, 4)

def test_filterNot(lst):
    assert lst.filterNot(lambda i: i % 2 == 0) == (1, 3)

def test_find(lst, lst1):
    assert lst.find(lambda i: i == 2) == 2
    assert lst1.find(lambda i: i == "a") == "a"

def test_flatten(lst, lst1):
    unflat = Iterable(lst, lst1)
    assert unflat.flatten == Iterable(1, 2, 3, 4, "a", "b", "c", "d")

def test_foldLeft(lst):
    assert lst.foldLeft(0)(lambda a, b: a + b) == sum(lst)
    product = 1
    for i in lst: product *= i
    assert lst.foldLeft(1)(lambda a, b: a * b) == product

def test_forall(lst, lst1):
    assert lst.forall(lambda i:0 <  i < 5), lst
    assert lst1.forall(lambda i: len(i) == 1), lst

def test_head(lst):
    with pytest.raises(IndexError):
        assert Iterable().head
    assert lst.head == lst(0) == lst[0]

def test_headOption(lst):
    assert lst.headOption == lst(0) == lst[0]
    assert Iterable().headOption is None

def test_drop(lst):
    assert lst.drop(2) == (1, 2)
    assert lst.drop(1) == (1,)

def test_dropRight(lst):
    assert lst.dropRight(2) == (3, 4)
    assert lst.dropRight(1) == (4,)

def test_map(lst, lst1):
    assert lst.map(lambda i: i * 2) == (2, 4, 6, 8)
    assert lst1.map(lambda i: i * 2) == ("aa", "bb", "cc", "dd")

def test_isEmpty(lst):
    assert not lst.isEmpty
    assert lst.empty.isEmpty
    assert Iterable().isEmpty

def test_mkString(lst):
    assert lst.mkString(", ") == "1, 2, 3, 4"
    assert lst.mkString(", ", start="Iterable(", end=")") == "Iterable(1, 2, 3, 4)" == str(lst)

def test_partition(lst, is_even):
    assert lst.partition(is_even) == (Iterable(2, 4), Iterable(1, 3))
    assert lst.map(is_even).partition(lambda i: i) == (Iterable(True, True), Iterable(False, False))

def test_reverse(lst):
    assert lst.reverse == tuple(reversed(lst)) == tuple(lst[::-1])

def test_size(lst):
    assert lst.size == len(tuple(lst)) == len(lst)

def test_zip(lst):
    assert lst.zipWithIndex == tuple(zip(lst, range(len(lst))))
    assert lst.zip(range(lst.size)) == tuple(zip(lst, range(lst.size)))

def test_unzip(lst, lst1):
    assert lst.zipWithIndex.unzip == ((1, 2, 3, 4), (0, 1, 2, 3))
    assert lst.zip(lst1).zipWithIndex.map(
            lambda i: (i[1], i[0][0], i[0][1])) == (
                        (0, 1, 'a'), (1, 2, 'b'), (2, 3, 'c'), (3, 4, 'd'))
