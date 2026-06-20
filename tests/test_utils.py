# -*- coding: utf-8 -*-
"""Utility unit tests."""

import pytest
from dribdat.utils import unpack_csvlist

def test_unpack_csvlist_empty():
    assert unpack_csvlist(None) == []
    assert unpack_csvlist("") == []

def test_unpack_csvlist_normal():
    assert unpack_csvlist("a,b,c") == ["a", "b", "c"]

def test_unpack_csvlist_whitespace():
    assert unpack_csvlist(" a , b,c  ") == ["a", "b", "c"]

def test_unpack_csvlist_duplicate():
    assert unpack_csvlist("a,b,a,c,b") == ["a", "b", "c"]

def test_unpack_csvlist_custom_separator():
    assert unpack_csvlist("a|b|c", sep="|") == ["a", "b", "c"]
    assert unpack_csvlist("a;b;a", sep=";") == ["a", "b"]

def test_unpack_csvlist_empty_elements():
    assert unpack_csvlist("a,,b") == ["a", "", "b"]
    assert unpack_csvlist("a, ,b") == ["a", "", "b"]
