import miniops


def test_native_backend_active():
    assert miniops.BACKEND == "native"
