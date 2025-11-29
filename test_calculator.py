from app.main import compute
import pytest


def test_add():
    assert compute(2, 3, "add") == 5


def test_subtract():
    assert compute(5, 2, "sub") == 3


def test_multiply():
    assert compute(4, 3, "mul") == 12


def test_divide():
    assert compute(10, 2, "div") == 5


def test_divide_by_zero():
    with pytest.raises(ValueError):
        compute(1, 0, "div")


def test_unknown_op():
    with pytest.raises(ValueError):
        compute(1, 2, "???")
