from app.add import add

def test_add_ints():
    assert add(2, 3) == 5

def test_add_floats():
    assert add(1.5, 2.25) == 3.75

