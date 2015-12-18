import pytest


def test_pass_1():
    assert 1


def test_fail_1():
    assert 0


def test_fail_2():
    assert 0


def test_skip_1():
    pytest.skip()
