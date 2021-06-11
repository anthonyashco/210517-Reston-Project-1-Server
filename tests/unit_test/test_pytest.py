def test_pass():
    phrase = "pass"
    assert phrase == "pass"


def test_fail():
    phrase = "fail"
    try:
        assert phrase == "pass"
        return False
    except AssertionError as e:
        print(e)
        return True
