from icc_est import estimate_icc


def test_perfect_agreement_returns_one():
    data = [
        [5.0, 5.0, 5.0],
        [5.0, 5.0, 5.0],
        [5.0, 5.0, 5.0],
    ]
    assert estimate_icc(data) == 1.0


def test_high_reliability_is_positive():
    data = [
        [1.0, 2.0, 3.0],
        [2.0, 3.0, 4.0],
        [3.0, 4.0, 5.0],
    ]
    assert estimate_icc(data) > 0.7


def test_uneven_group_sizes_are_rejected():
    data = [
        [1.0, 2.0, 3.0],
        [2.0, 3.0],
    ]
    try:
        estimate_icc(data)
        raise AssertionError("Expected ValueError for uneven group lengths")
    except ValueError:
        pass
