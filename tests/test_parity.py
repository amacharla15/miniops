import math

import miniops
from miniops import reference


def assert_float_lists_close(a, b, tol=1e-9):
    assert len(a) == len(b)
    i = 0
    while i < len(a):
        assert math.isclose(a[i], b[i], rel_tol=tol, abs_tol=tol)
        i += 1


def test_vector_add_parity_basic():
    x = [1.0, 2.0, 3.0]
    y = [4.0, 5.0, 6.0]

    native_result = miniops.vector_add(x, y)
    reference_result = reference.vector_add(x, y)

    assert native_result == reference_result


def test_vector_add_parity_negative_values():
    x = [-1.5, 2.0, -3.25]
    y = [4.0, -5.5, 6.25]

    native_result = miniops.vector_add(x, y)
    reference_result = reference.vector_add(x, y)

    assert native_result == reference_result


def test_topk_parity_basic():
    x = [1.0, 5.0, 3.0, 4.0]

    native_values, native_indices = miniops.topk(x, 2)
    reference_values, reference_indices = reference.topk(x, 2)

    assert native_values == reference_values
    assert native_indices == reference_indices


def test_topk_parity_duplicates():
    x = [4.0, 4.0, 2.0, 1.0]

    native_values, native_indices = miniops.topk(x, 2)
    reference_values, reference_indices = reference.topk(x, 2)

    assert native_values == reference_values
    assert native_indices == reference_indices


def test_softmax_parity_basic():
    x = [1.0, 2.0, 3.0]

    native_result = miniops.softmax(x)
    reference_result = reference.softmax(x)

    assert_float_lists_close(native_result, reference_result)


def test_softmax_parity_mixed_values():
    x = [-2.0, 0.5, 3.0, -1.0]

    native_result = miniops.softmax(x)
    reference_result = reference.softmax(x)

    assert_float_lists_close(native_result, reference_result)


def test_vector_add_error_parity():
    x = [1.0]
    y = [1.0, 2.0]

    try:
        miniops.vector_add(x, y)
        assert False
    except ValueError:
        pass

    try:
        reference.vector_add(x, y)
        assert False
    except ValueError:
        pass


def test_topk_error_parity_zero_k():
    x = [1.0, 2.0, 3.0]

    try:
        miniops.topk(x, 0)
        assert False
    except ValueError:
        pass

    try:
        reference.topk(x, 0)
        assert False
    except ValueError:
        pass


def test_topk_error_parity_k_too_large():
    x = [1.0, 2.0]

    try:
        miniops.topk(x, 3)
        assert False
    except ValueError:
        pass

    try:
        reference.topk(x, 3)
        assert False
    except ValueError:
        pass


def test_softmax_error_parity_empty():
    x = []

    try:
        miniops.softmax(x)
        assert False
    except ValueError:
        pass

    try:
        reference.softmax(x)
        assert False
    except ValueError:
        pass