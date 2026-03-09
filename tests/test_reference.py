import math

import miniops


def test_vector_add_basic():
    result = miniops.vector_add([1.0, 2.0], [3.0, 4.0])
    assert result == [4.0, 6.0]


def test_vector_add_length_mismatch():
    try:
        miniops.vector_add([1.0], [1.0, 2.0])
        assert False
    except ValueError:
        assert True


def test_topk_basic():
    values, indices = miniops.topk([1.0, 5.0, 3.0, 4.0], 2)
    assert values == [5.0, 4.0]
    assert indices == [1, 3]


def test_softmax_basic():
    result = miniops.softmax([1.0, 2.0, 3.0])
    assert len(result) == 3
    assert math.isclose(sum(result), 1.0, rel_tol=1e-9, abs_tol=1e-9)


def test_softmax_order():
    result = miniops.softmax([1.0, 2.0, 3.0])
    assert result[2] > result[1] > result[0]