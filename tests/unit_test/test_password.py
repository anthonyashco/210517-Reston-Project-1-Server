from utils.password import Password as p


def test_salt():
    """Generate 100 salts and ensure none are repeating."""
    salts = []
    try:
        for _ in range(100):
            salts.append(p.salt_shaker())
        for i, salt in enumerate(salts):
            for j in range(i + 1, len(salts)):
                assert salt != salts[j]
    except ImportError:
        return False


def test_generate_password():
    griddle = p.hash_griddle("potato")
    assert p.check_pass("potato", griddle[0], griddle[1])
    assert not p.check_pass("potahto", griddle[0], griddle[1])


def test_saved_password():
    pass_hash = "153417bd132637ba71cf236c323a55bd"
    pass_salt = "71a8b28bf9986f51ab5e31c1c20993f3"
    assert p.check_pass("password", pass_hash, pass_salt)
    assert not p.check_pass("potato", pass_hash, pass_salt)
